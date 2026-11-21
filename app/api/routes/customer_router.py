from fastapi import APIRouter, Depends

from app.api.routes.auth_router import current_user
from app.schemas.customer import CustomerResponse, CustomerUpdate
from app.services.commerce_services import customer_service


router = APIRouter(tags=["Customers"])
service = customer_service

ERROR_401 = {401: {"description": "Authentication required or invalid credentials"}}
ERROR_403 = {403: {"description": "Account deactivated or access forbidden"}}


@router.get(
    "/customers/me",
    response_model=CustomerResponse,
    responses={**ERROR_401, **ERROR_403},
)
def me(user=Depends(current_user)):
    return {key: value for key, value in user.items() if key not in ("password_hash", "salt")}


@router.patch(
    "/customers/me",
    response_model=CustomerResponse,
    responses={**ERROR_401, **ERROR_403},
)
def update(data: CustomerUpdate, user=Depends(current_user)):
    return service.update_customer(user["id"], data.model_dump(exclude_none=True))


@router.delete(
    "/customers/me",
    status_code=204,
    responses={**ERROR_401, **ERROR_403},
)
def deactivate(user=Depends(current_user)):
    service.deactivate(user["id"])