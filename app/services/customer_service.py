from app.repositories.commerce_repository import CommerceRepository


def safe_customer(customer):
    return {k: v for k, v in customer.items() if k not in ("password_hash", "salt")}


class CustomerService:
    def __init__(self, repo=None):
        self.repo = repo or CommerceRepository()

    def update_customer(self, customer_id, changes):
        with self.repo.lock:
            db = self.repo.read()
            customer = db["customers"][customer_id]
            customer.update(changes)
            self.repo.save(db)
            return safe_customer(customer)

    def deactivate(self, customer_id):
        with self.repo.lock:
            db = self.repo.read()
            db["customers"][customer_id]["active"] = False
            db["carts"].pop(customer_id, None)
            self.repo.save(db)
