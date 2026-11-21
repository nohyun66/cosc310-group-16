from pydantic import BaseModel, Field

class CustomerResponse(BaseModel):
    id: str
    email: str
    name: str
    address: str
    active: bool
    role: str

class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    address: str | None = Field(default=None, min_length=1)