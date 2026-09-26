from fastapi import FastAPI
from app.api.routes.restaurant_router import router as restaurant_router

app = FastAPI(
    title="COSC 310 Group 16",
    version="0.1.0"
)

app.include_router(restaurant_router)

@app.get("/health")
def health():
    return {"status": "ok"}