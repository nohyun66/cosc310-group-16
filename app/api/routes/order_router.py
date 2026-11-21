from fastapi import APIRouter, Depends

from app.api.routes.auth_router import current_user
from app.schemas.order import OrderResponse
from app.services.commerce_services import order_service


router = APIRouter(tags=["Orders"])
service = order_service

ERROR_401 = {401: {"description": "Authentication required or invalid credentials"}}
ERROR_403 = {403: {"description": "Account deactivated or access forbidden"}}
ERROR_404 = {404: {"description": "Requested resource not found"}}


@router.get(
    "/orders",
    response_model=list[OrderResponse],
    responses={**ERROR_401, **ERROR_403},
)
def orders(user=Depends(current_user)):
    return service.list_orders(user["id"])


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    responses={**ERROR_401, **ERROR_403, **ERROR_404},
)
def order(order_id: str, user=Depends(current_user)):
    return service.get_order(user["id"], order_id)
