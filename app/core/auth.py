# This is to check the user's role before allowing restaurant changes.
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.routes import commerce_router

bearer = HTTPBearer(auto_error=False)


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    token = credentials.credentials if credentials else None
    return commerce_router.service.authenticated(token)


def require_admin(user: dict = Depends(current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return user
