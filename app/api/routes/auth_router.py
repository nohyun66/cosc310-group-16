from fastapi import APIRouter, Depends

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.security import get_current_customer
from app.schemas.customer import Customer

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Sign in",
    description="Verify customer credentials and return a token valid for 30 minutes.",
    responses={
        401: {"description": "Incorrect email or password."},
        403: {"description": "Customer account is deactivated."},
        503: {"description": "Authentication is not configured."},
    },
)
def login(details: LoginRequest):
    return AuthService().login(details)

@router.get(
    "/me",
    response_model=Customer,
    summary="Get the signed-in customer",
    description="Return the current customer's information using a valid bearer token.",
    responses={
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Customer account is deactivated."},
        503: {"description": "Authentication is not configured."},
    },
)
def get_me(
    customer: Customer = Depends(get_current_customer),
):
    return customer