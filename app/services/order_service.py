from app.repositories.commerce_repository import CommerceRepository
from app.services.util import fail


class OrderService:
    def __init__(self, repo=None):
        self.repo = repo or CommerceRepository()

    def get_order(self, customer_id, order_id):
        order = self.repo.read()["orders"].get(order_id)
        if not order:
            fail(404, "Order not found")
        if order["customer_id"] != customer_id:
            fail(403, "Order belongs to another customer")
        return order

    def list_orders(self, customer_id):
        return [
            o
            for o in self.repo.read()["orders"].values()
            if o["customer_id"] == customer_id
        ]
