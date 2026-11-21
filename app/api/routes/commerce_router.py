
from fastapi import APIRouter, Depends
from app.core.auth import current_user
from app.core.dependencies import commerce_service as service
from app.schemas.commerce import (
    RegisterInput, LoginInput, CustomerUpdate, CartAdd, QuantityUpdate,
    CustomerResponse, TokenResponse, CartResponse, OrderResponse
)

router = APIRouter(tags=['M2 Commerce'])


ERROR_401 = {401: {'description': 'Authentication required or invalid credentials'}}
ERROR_403 = {403: {'description': 'Account deactivated or access forbidden'}}
ERROR_404 = {404: {'description': 'Requested resource not found'}}
ERROR_409 = {409: {'description': 'Business rule conflict'}}


@router.post('/customers/register', response_model=CustomerResponse, status_code=201, responses=ERROR_409, summary='Register a new customer')
def register(data: RegisterInput):
    return service.register(data)


@router.post('/customers/login', response_model=TokenResponse, responses=ERROR_401, summary='Sign in and obtain a bearer token')
def login(data: LoginInput):
    return service.login(data.email, data.password)


@router.get('/customers/me', response_model=CustomerResponse, responses={**ERROR_401, **ERROR_403}, summary='Retrieve the authenticated customer')
def me(user=Depends(current_user)):
    return {k: v for k, v in user.items() if k not in ('password_hash', 'salt')}


@router.patch('/customers/me', response_model=CustomerResponse, responses={**ERROR_401, **ERROR_403}, summary='Update name or delivery address')
def update(data: CustomerUpdate, user=Depends(current_user)):
    return service.update_customer(user['id'], data.model_dump(exclude_none=True))


@router.delete('/customers/me', status_code=204, responses={**ERROR_401, **ERROR_403}, summary='Deactivate customer account')
def deactivate(user=Depends(current_user)):
    service.deactivate(user['id'])


@router.get('/cart', response_model=CartResponse, responses={**ERROR_401, **ERROR_403, **ERROR_404}, summary='Retrieve cart and authoritative totals')
def get_cart(user=Depends(current_user)):
    return service.cart(user['id'])


@router.post('/cart/items', response_model=CartResponse, responses={**ERROR_401, **ERROR_403, **ERROR_404, **ERROR_409}, summary='Add a menu item to the active cart')
def add_item(data: CartAdd, user=Depends(current_user)):
    return service.add(user['id'], data.item_id, data.quantity)


@router.put('/cart/items/{item_id}', response_model=CartResponse, responses={**ERROR_401, **ERROR_403, **ERROR_404, **ERROR_409}, summary='Change an item quantity')
def change_item(item_id: str, data: QuantityUpdate, user=Depends(current_user)):
    return service.change(user['id'], item_id, data.quantity)


@router.delete('/cart/items/{item_id}', response_model=CartResponse, responses={**ERROR_401, **ERROR_403, **ERROR_404}, summary='Remove an item from the cart')
def remove_item(item_id: str, user=Depends(current_user)):
    return service.remove(user['id'], item_id)


@router.delete('/cart', response_model=CartResponse, responses={**ERROR_401, **ERROR_403}, summary='Clear the active cart')
def clear_cart(user=Depends(current_user)):
    return service.clear(user['id'])


@router.post('/checkout', response_model=OrderResponse, status_code=201, responses={**ERROR_401, **ERROR_403, **ERROR_404, **ERROR_409}, summary='Validate and persist order before clearing cart')
def checkout(user=Depends(current_user)):
    return service.checkout(user['id'])


@router.get('/orders', response_model=list[OrderResponse], responses={**ERROR_401, **ERROR_403}, summary='List orders belonging to signed-in customer')
def orders(user=Depends(current_user)):
    return service.list_orders(user['id'])


@router.get(
    '/orders/{order_id}',
    response_model=OrderResponse,
    responses={**ERROR_401, **ERROR_403, **ERROR_404},
    summary='Retrieve an order'
)
def order(order_id: str, user=Depends(current_user)):
    return service.get_order(user['id'], order_id)