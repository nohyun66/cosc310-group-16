from fastapi import FastAPI
from app.api.routes.restaurant_router import router as restaurant_router
from app.schemas.health import HealthResponse

app = FastAPI(
    title="COSC 310 Group 16",
    version="0.1.0"
)

app.include_router(restaurant_router)

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API health",
    description="Confirm the API is running and responding to requests",
)
def health():
    return {"status": "ok"}