from fastapi import APIRouter

from app.schemas.authorization import LoginInput, RegisterInput, TokenResponse
from app.schemas.customer import CustomerResponse
from app.services.commerce_services import auth_service

router = APIRouter(tags=["Authentication"])
service = auth_service

ERROR_401 = {
    401: {"description": "Authentication required or invalid credentials"}
}
ERROR_409 = {
    409: {"description": "Business rule conflict"}
}


@router.post(
    "/customers/register",
    response_model=CustomerResponse,
    status_code=201,
    responses=ERROR_409,
)
def register(data: RegisterInput):
    return service.register(data)


@router.post(
    "/customers/login",
    response_model=TokenResponse,
    responses=ERROR_401,
)
def login(data: LoginInput):
    return service.login(data.email, data.password)