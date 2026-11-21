from fastapi import APIRouter, Depends

from app.api.routes.auth_router import current_user
from app.schemas.cart import CartAdd, CartResponse, QuantityUpdate
from app.schemas.order import OrderResponse
from app.services.commerce_services import cart_service


router = APIRouter(tags=["Cart"])
service = cart_service

ERROR_401 = {401: {"description": "Authentication required or invalid credentials"}}
ERROR_403 = {403: {"description": "Account deactivated or access forbidden"}}
ERROR_404 = {404: {"description": "Requested resource not found"}}
ERROR_409 = {409: {"description": "Business rule conflict"}}


@router.get(
    "/cart",
    response_model=CartResponse,
    responses={**ERROR_401, **ERROR_403, **ERROR_404},
)
def get_cart(user=Depends(current_user)):
    return service.cart(user["id"])


@router.post(
    "/cart/items",
    response_model=CartResponse,
    responses={**ERROR_401, **ERROR_403, **ERROR_404, **ERROR_409},
)
def add_item(data: CartAdd, user=Depends(current_user)):
    return service.add(user["id"], data.item_id, data.quantity)


@router.put(
    "/cart/items/{item_id}",
    response_model=CartResponse,
    responses={**ERROR_401, **ERROR_403, **ERROR_404, **ERROR_409},
)
def change_item(item_id: str, data: QuantityUpdate, user=Depends(current_user)):
    return service.change(user["id"], item_id, data.quantity)


@router.delete(
    "/cart/items/{item_id}",
    response_model=CartResponse,
    responses={**ERROR_401, **ERROR_403, **ERROR_404},
)
def remove_item(item_id: str, user=Depends(current_user)):
    return service.remove(user["id"], item_id)


@router.delete(
    "/cart",
    response_model=CartResponse,
    responses={**ERROR_401, **ERROR_403},
)
def clear_cart(user=Depends(current_user)):
    return service.clear(user["id"])


@router.post(
    "/checkout",
    response_model=OrderResponse,
    status_code=201,
    responses={**ERROR_401, **ERROR_403, **ERROR_404, **ERROR_409},
)
def checkout(user=Depends(current_user)):
    return service.checkout(user["id"])
