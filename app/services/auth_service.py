from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

from app.core import config
from app.repositories.customer_repository import CustomerRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.customer_service import password_hash


class AuthService:
    def __init__(self):
        self.repository = CustomerRepository()

    def login(self, details: LoginRequest) -> TokenResponse:
        customer = self.repository.get_by_email(details.email)

        if customer is None:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
            )

        if not password_hash.verify(
            details.password, customer.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
            )

        if not customer.is_active:
            raise HTTPException(
                status_code=403,
                detail="Customer account is deactivated",
            )

        if not config.JWT_SECRET_KEY:
            raise HTTPException(
                status_code=503,
                detail="Authentication is not configured",
            )

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        token = jwt.encode(
            {
                "sub": customer.id,
                "exp": expires_at,
            },
            config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )

        return TokenResponse(access_token=token)