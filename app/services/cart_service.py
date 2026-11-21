from datetime import datetime, timezone
from uuid import uuid4

from app.repositories.commerce_repository import CommerceRepository
from app.services.util import fail
from app.services.item_service import ItemService
from app.services.restaurant_service import RestaurantService


class CartService:
    def __init__(self, repo=None):
        self.repo = repo or CommerceRepository()
        self.item_service = ItemService()
        self.restaurant_service = RestaurantService()

    def _view_cart(self, cart):
        lines = []
        subtotal = 0
        for item_id, quantity in cart.get("items", {}).items():
            item = self.item_service.get_item(item_id)
            unit = int(item.price)
            lines.append(
                {
                    "item_id": item_id,
                    "name": item.name,
                    "quantity": quantity,
                    "unit_price_cents": unit,
                    "line_total_cents": quantity * unit,
                }
            )
            subtotal += quantity * unit
        return {
            "restaurant_id": cart.get("restaurant_id"),
            "items": lines,
            "subtotal_cents": subtotal,
            "total_cents": subtotal,
        }

    def cart(self, customer_id):
        db = self.repo.read()
        cart = db["carts"].get(customer_id, {"restaurant_id": None, "items": {}})
        return self._view_cart(cart)

    def add(self, customer_id, item_id, quantity):
        if quantity < 1:
            fail(422, "Quantity must be positive")
        with self.repo.lock:
            item = self.item_service.get_available_item(item_id)
            rid = str(item.restaurant_id)
            self.restaurant_service.get_open_restaurant(rid)
            db = self.repo.read()
            cart = db["carts"].setdefault(
                customer_id, {"restaurant_id": rid, "items": {}}
            )
            if cart["restaurant_id"] not in (None, rid):
                fail(409, "Cart must contain items from one restaurant")
            cart["restaurant_id"] = rid
            cart["items"][item_id] = cart["items"].get(item_id, 0) + quantity
            self.repo.save(db)
            return self._view_cart(cart)

    def change(self, customer_id, item_id, quantity):
        if quantity < 1:
            fail(422, "Quantity must be positive; use DELETE to remove")
        with self.repo.lock:
            db = self.repo.read()
            cart = db["carts"].get(customer_id)
            if not cart or item_id not in cart["items"]:
                fail(404, "Item not in cart")
            item = self.item_service.get_available_item(item_id)
            self.restaurant_service.get_open_restaurant(item.restaurant_id)
            cart["items"][item_id] = quantity
            self.repo.save(db)
            return self._view_cart(cart)

    def remove(self, customer_id, item_id):
        with self.repo.lock:
            db = self.repo.read()
            cart = db["carts"].get(customer_id)
            if not cart or item_id not in cart["items"]:
                fail(404, "Item not in cart")
            del cart["items"][item_id]
            if not cart["items"]:
                cart["restaurant_id"] = None
            self.repo.save(db)
            return self._view_cart(cart)

    def clear(self, customer_id):
        with self.repo.lock:
            db = self.repo.read()
            db["carts"].pop(customer_id, None)
            self.repo.save(db)
            return {
                "restaurant_id": None,
                "items": [],
                "subtotal_cents": 0,
                "total_cents": 0,
            }

    def checkout(self, customer_id):
        with self.repo.lock:
            db = self.repo.read()
            customer = db["customers"].get(customer_id)
            if not customer or not customer["active"] or not customer["address"]:
                fail(409, "Active customer with address required")
            cart = db["carts"].get(customer_id)
            if not cart or not cart["items"]:
                fail(409, "Cart is empty")
            self.restaurant_service.get_open_restaurant(cart["restaurant_id"])
            for item_id, qty in cart["items"].items():
                if (
                    qty < 1
                    or str(self.item_service.get_available_item(item_id).restaurant_id)
                    != cart["restaurant_id"]
                ):
                    fail(409, "Invalid cart contents")
            view = self._view_cart(cart)
            order = {
                "id": str(uuid4()),
                "customer_id": customer_id,
                "restaurant_id": cart["restaurant_id"],
                "delivery_address": customer["address"],
                "items": view["items"],
                "subtotal_cents": view["subtotal_cents"],
                "total_cents": view["total_cents"],
                "status": "created",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            db["orders"][order["id"]] = order
            db["carts"].pop(customer_id, None)
            self.repo.save(db)
            return order
