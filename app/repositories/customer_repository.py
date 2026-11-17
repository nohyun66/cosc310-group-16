import json
from pathlib import Path

from app.schemas.customer import CustomerRecord

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "customers.json"


class CustomerRepository:
    def get_all_customers(self) -> list[CustomerRecord]:
        with open(DATA_PATH, encoding="utf-8") as data_file:
            records = json.load(data_file)

        return [CustomerRecord(**record) for record in records]

    def get_by_id(self, customer_id: str) -> CustomerRecord | None:
        for customer in self.get_all_customers():
            if customer.id == customer_id:
                return customer
        return None

    def get_by_email(self, email: str) -> CustomerRecord | None:
        email = email.strip().lower()

        for customer in self.get_all_customers():
            if customer.email.lower() == email:
                return customer
        return None

    def create_customer(self, customer: CustomerRecord) -> CustomerRecord:
        customers = self.get_all_customers()
        customers.append(customer)

        with open(DATA_PATH, "w", encoding="utf-8") as data_file:
            json.dump(
                [record.model_dump(mode="json") for record in customers],
                data_file,
                indent=2,
            )

        return customer