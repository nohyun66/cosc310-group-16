from fastapi import APIRouter

from app.schemas.customer import Customer, CustomerCreate
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "",
    response_model=Customer,
    status_code=201,
    summary="Register a customer",
    description=(
        "Create a customer account and save its details. "
        "The password and password hash are never returned."
    ),
    responses={
        409: {"description": "Email is already registered."},
        422: {"description": "Registration details are invalid."},
    },
)
def register_customer(details: CustomerCreate):
    return CustomerService().register_customer(details)