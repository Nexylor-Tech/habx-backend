import json
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from standardwebhooks.webhooks import Webhook

from app.config import settings
from app.db import user_collection
from app.dodo_client import client

product_ids = {
    "premium": settings.PRODUCT_ID_PREMIUM,
    "elite": settings.PRODUCT_ID_ELITE,
}


async def create_checkout_session(data, user: dict) -> dict:
    if not client.dodo_client:
        raise HTTPException(status_code=503, detail="Payment service is unavailable")

    tier = data.tier.lower()
    if tier not in product_ids:
        raise HTTPException(status_code=400, detail="Invalid tier")

    product_id = product_ids[tier]

    try:
        product = await client.dodo_client.products.retrieve(product_id)
        product_metadata = product.metadata or {}
        customer = await client.dodo_client.customers.retrieve(user["dodo_customer_id"])
        ai_generation_limit = product_metadata.get("ai_limit", 10)
        workspace_limit = product_metadata.get("workspace_limit", 1)
        plan = product_metadata.get("plan", "free")
        session = await client.dodo_client.checkout_sessions.create(
            product_cart=[
                {
                    "product_id": product_id,
                    "quantity": 1,
                }
            ],
            billing_address=None,
            customer={
                "customer_id": customer.customer_id,
            },
            metadata={
                "user_id": str(user["_id"]),
                "ai_generation_limit": str(ai_generation_limit),
                "workspace_limit": str(workspace_limit),
                "plan": plan,
            },
            return_url="http://localhost:3000/home/",
        )
        return {
            "checkout_url": session.checkout_url,
            "session_id": session.session_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment service error: {str(e)}")


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
        raise HTTPException(status_code=500, detail=f"Payment service error: {str(e)}")


async def dodo_webhook(req):
    payload_bytes = await req.body()
    payload_str = payload_bytes.decode("utf-8")
    webhook_id = req.headers.get("webhook-id")
    webhook_signature = req.headers.get("webhook-signature")
    webhook_timestamp = req.headers.get("webhook-timestamp")

    if not all([webhook_id, webhook_signature, webhook_timestamp]):
        raise HTTPException(status_code=400, detail="Missing webhook headers")

    try:
        wh = Webhook(settings.DODO_WEBHOOK_SECRET.get_secret_value())

        wh.verify(
            payload_str,
            {
                "webhook-id": webhook_id,
                "webhook-signature": webhook_signature,
                "webhook-timestamp": webhook_timestamp,
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Invalid webhook signature {str(e)}"
        )
    try:
        event = json.loads(payload_str)

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event_type = event.get("type")
    data = event.get("data") or {}

    metadata = data.get("metadata") or {}
    customer = data.get("customer") or {}

    user_id = metadata.get("user_id")
    email = customer.get("email")

    query = None

    if user_id:
        try:
            query = {"_id": ObjectId(user_id)}
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid user id")

    elif email:
        query = {"email": email}

    if not query:
        return {"message": "No user found"}

    if event_type in ["subscription.active", "subscription.renewed"]:
        ai_generation_limit = metadata.get("ai_generation_limit")
        workspace_limit = metadata.get("workspace_limit")
        plan = metadata.get("plan")

        await user_collection.update_one(
            query,
            {
                "$set": {
                    "is_premium": True,
                    "subscription_tier": plan,
                    "ai_generation_limit": ai_generation_limit,
                    "workspace_limit": workspace_limit,
                    "plan": plan,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )

    elif event_type in ["subscription.cancelled", "subscription.failed"]:
        await user_collection.update_one(
            query,
            {
                "$set": {
                    "is_premium": False,
                    "subscription_tier": "free",
                    "ai_generation_limit": 10,
                    "workspace_limit": 1,
                    "plan": "free",
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )

    return {"status": "success"}
