from pydantic import BaseModel, Field

class RegisterInput(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)
    address: str = Field(min_length=1)

class LoginInput(BaseModel):
    email: str
    password: str

class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    address: str | None = Field(default=None, min_length=1)

class CartAdd(BaseModel):
    item_id: str
    quantity: int = Field(gt=0)

class QuantityUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CustomerResponse(BaseModel):
    id: str
    email: str
    name: str
    address: str
    active: bool
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


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
