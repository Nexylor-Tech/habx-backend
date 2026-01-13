import json
from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from dodopayments import AsyncDodoPayments
from fastapi import HTTPException
from standardwebhooks.webhooks import Webhook

from app.config import settings
from app.db import user_collection
from app.dodo_client import client

product_ids = {
    "premium": settings.PRODUCT_ID_PREMIUM,
    "elite": settings.PRODUCT_ID_ELITE,
}


async def create_checkout_session(data, user_id: dict) -> dict:
    if not client.dodo_client:
        raise HTTPException(status_code=503, detail="Payment service is unavailable")

    tier = data.tier.lower()
    if tier not in product_ids:
        raise HTTPException(status_code=400, detail="Invalid tier")

    product_id = product_ids[tier]

    try:
        session = await client.dodo_client.checkout_sessions.create(
            product_cart=[
                {
                    "product_id": product_id,
                    "quantity": 1,
                }
            ],
            billing_address=None,
            customer={
                "email": user_id["email"],
                "name": user_id.get("name", None),
                "customer_id": user_id.get("dodo_customer_id"),
            },
            metadata={"user_id": str(user_id["_id"]), "target_tier": tier},
            return_url="http://localhost:3000/home/",
        )
        return {
            "checkout_url": session.checkout_url,
            "session_id": session.session_id,
        }
    except Exception as e:
        print(f"Dodo error: {e}")
        raise HTTPException(status_code=500, detail="Payment service error")


async def cancel_subscription(user_id: ObjectId, sub_id: str):
    try:
        await client.dodo_client.subscriptions.update(
            subscription_id=sub_id, cancel_at_next_billing_date=True
        )
        await user_collection.update_one(
            {"_id": user_id}, {"$set": {"subscription_status": "cancelled"}}
        )

        return {"message": "Subscription cancelled"}
    except Exception as e:
        print(f"Dodo error: {e}")
        raise HTTPException(status_code=500, detail="Payment service error")


async def dodo_webhook(req):
    payload_bytes = await req.body()
    payload_str = payload_bytes.decode("utf-8")

    webhook_id = req.headers.get("webhook-id")
    webhook_signature = req.headers.get("webhook-signature")
    webhook_timestamp = req.headers.get("webhook-timestamp")

    if not all([webhook_id, webhook_signature, webhook_timestamp]):
        raise HTTPException(status_code=400, detail="Missing required headers")

    try:
        wh = Webhook(settings.DODO_WEBHOOK_SECRET)
        wh.verify(
            payload_str,
            {
                "webhook-id": webhook_id,
                "webhook-signature": webhook_signature,
                "webhook-timestamp": webhook_timestamp,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid webhook signature {e}")

    try:
        event = json.load(payload_str)
        event_type = event.get("type")
        data = event.get("data", {})

        if event_type in ["subscription.active", "subscription.renewed"]:
            user_id = data.get("metadata", {}).get("user_id")
            email = data.get("customer", {}).get("email")

            query = None
            if user_id:
                query = {"_id": ObjectId(user_id)}
            elif email:
                query = {"email": email}

            if query:
                target_tier = data.get("metadata", {}).get("target_tier", "premium")
                await user_collection.update_one(
                    query,
                    {
                        "$set": {
                            "is_premium": True,
                            "subscription_tier": target_tier,
                            "dodo_customer_id": data.get("customer_id"),
                            "dodo_subscription_id": data.get("subscription_id"),
                            "updated_at": datetime.now(timezone.utc),
                        }
                    },
                )
        elif event_type in [
            "subscription.cancelled",
            "subscription.failed",
            "subscription.active",
        ]:
            user_id = data.get("metadata", {}).get("user_id")
            email = data.get("customer", {}).get("email")

            query = None
            if user_id:
                query = {"_id": ObjectId(user_id)}
            elif email:
                query = {"email": email}

            if query:
                await user_collection.update_one(
                    query,
                    {
                        "$set": {
                            "is_premium": False,
                            "subscription_tier": "free",
                            "updated_at": datetime.now(timezone.utc),
                        }
                    },
                )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User updated successfully"}
