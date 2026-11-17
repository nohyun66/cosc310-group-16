from typing import Literal

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    password: str = Field(min_length=8, max_length=128)
    delivery_address: str = Field(min_length=1)


class Customer(BaseModel):
    id: str
    name: str
    email: str
    delivery_address: str
    is_active: bool = True
    role: Literal["customer", "admin"] = "customer"


class CustomerRecord(Customer):
    password_hash: str