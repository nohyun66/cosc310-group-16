from uuid import uuid4

from fastapi import HTTPException
from pwdlib import PasswordHash

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import Customer, CustomerCreate, CustomerRecord

password_hash = PasswordHash.recommended()


class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    def register_customer(self, details: CustomerCreate) -> Customer:
        email = details.email.strip().lower()
        name = details.name.strip()
        address = details.delivery_address.strip()

        if not name or not address:
            raise HTTPException(
                status_code=422,
                detail="Name and delivery address cannot be blank",
            )

        if not email or "@" not in email:
            raise HTTPException(
                status_code=422,
                detail="A valid email address is required",
            )

        if self.repository.get_by_email(email) is not None:
            raise HTTPException(
                status_code=409,
                detail="Email is already registered",
            )

        customer = CustomerRecord(
            id=str(uuid4()),
            name=name,
            email=email,
            delivery_address=address,
            password_hash=password_hash.hash(details.password),
        )

        saved = self.repository.create_customer(customer)

        return Customer(**saved.model_dump(exclude={"password_hash"}))