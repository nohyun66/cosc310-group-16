import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from app.core import config
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import Customer

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_customer(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> Customer:
    unauthorized = HTTPException(
        status_code=401,
        detail="A valid sign-in token is required",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    if not config.JWT_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Authentication is not configured",
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
    except InvalidTokenError:
        raise unauthorized

    customer_id = payload["sub"]

    if not isinstance(customer_id, str):
        raise unauthorized

    customer = CustomerRepository().get_by_id(customer_id)

    if customer is None:
        raise unauthorized

    if not customer.is_active:
        raise HTTPException(
            status_code=403,
            detail="Customer account is deactivated",
        )

    return Customer(
        **customer.model_dump(exclude={"password_hash"})
    )


def require_admin(
    customer: Customer = Depends(get_current_customer),
) -> Customer:
    if customer.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Administrator access is required",
        )

    return customer


def require_customer_owner(
    customer_id: str,
    customer: Customer = Depends(get_current_customer),
) -> Customer:
    if customer.id != customer_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another customer's data",
        )

    return customer