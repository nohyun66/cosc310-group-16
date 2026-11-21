# This is to check the user's role before allowing restaurant changes.
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.dependencies import commerce_service

bearer = HTTPBearer(auto_error=False)


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    token = credentials.credentials if credentials else None
    return commerce_service.authenticated(token)


def require_admin(user: dict = Depends(current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return user
