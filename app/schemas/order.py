from pydantic import BaseModel
from app.schemas.cart import CartItemResponse

class OrderResponse(BaseModel):
    id: str
    customer_id: str
    restaurant_id: str
    delivery_address: str
    items: list[CartItemResponse]
    subtotal_cents: int
    total_cents: int
    status: str
    created_at: str