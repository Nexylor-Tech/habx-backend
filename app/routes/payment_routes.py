from fastapi import APIRouter, BackgroundTasks, Depends, Request

from app.deps import auth
from app.models.payment import CheckoutRequest
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["Payment"])


@router.post("/checkout")
async def create_checkout_session(
    request: CheckoutRequest, current_user: dict = Depends(auth.get_current_user)
):
    return await payment_service.create_checkout_session(request, current_user)


@router.post("/webhook/dodo")
async def dodo_webhook(request: Request):
    return await payment_service.dodo_webhook(request)


@router.post("/subscription/cancel")
async def cancel_susbcription(current_user: dict = Depends(auth.get_current_user)):
    sub_id = current_user["dodo_subscription_id"]
    return await payment_service.cancel_subscription(current_user["_id"], sub_id)
