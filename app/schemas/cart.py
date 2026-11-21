from pydantic import BaseModel, Field

class CartAdd(BaseModel):
    item_id: str
    quantity: int = Field(gt=0)

class QuantityUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    item_id: str
    name: str
    quantity: int
    unit_price_cents: int
    line_total_cents: int

class CartResponse(BaseModel):
    restaurant_id: str | None
    items: list[CartItemResponse]
    subtotal_cents: int
    total_cents: int