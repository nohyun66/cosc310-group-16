from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes.restaurant_router import router as restaurant_router
from app.api.routes.item_router import router as item_router

app = FastAPI(
    title="COSC 310 Group 16",
    version="0.1.0"
)

app.include_router(restaurant_router)
app.include_router(item_router)

@app.get("/health")
def health():
    return {"status": "ok"}


app.mount(
    "/",
    StaticFiles(directory=Path(__file__).resolve().parents[1] / "web", html=True),
    name="web",
)