import hashlib
import hmac
import secrets
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException
from app.repositories.commerce_repository import CommerceRepository
from app.repositories.item_repository import ItemRepository
from app.repositories.restaurant_repository import RestaurantRepository


def fail(status, msg):
    raise HTTPException(status_code=status, detail=msg)


def safe_customer(customer):
    return {k: v for k, v in customer.items() if k not in ('password_hash', 'salt')}


class CommerceService:
    def __init__(self, repo=None, items=None, restaurants=None):
        self.repo = repo or CommerceRepository()
        self.items = items or ItemRepository()
        self.restaurants = restaurants or RestaurantRepository()
        self.sessions = {}

    def register(self, data):
        with self.repo.lock:
            db = self.repo.read()
            email = str(data.email).lower()
            if any(c['email'] == email for c in db['customers'].values()):
                fail(409, 'Email already registered')
            salt = secrets.token_hex(16)
            hashed = hashlib.pbkdf2_hmac('sha256', data.password.encode(), bytes.fromhex(salt), 200_000).hex()
            customer = {'id': str(uuid4()), 'email': email, 'name': data.name,
                        'address': data.address, 'active': True, 'role': 'customer',
                        'salt': salt, 'password_hash': hashed}
            db['customers'][customer['id']] = customer
            self.repo.save(db)
            return safe_customer(customer)

    def login(self, email, password):
        with self.repo.lock:
            customers = self.repo.read()['customers'].values()
            customer = next((c for c in customers if c['email'] == email.lower()), None)
            if not customer or not customer['active']:
                fail(401, 'Invalid credentials')
            proposed = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(customer['salt']), 200_000).hex()
            if not hmac.compare_digest(proposed, customer['password_hash']):
                fail(401, 'Invalid credentials')
            token = secrets.token_urlsafe(32)
            self.sessions[token] = customer['id']
            return {'access_token': token, 'token_type': 'bearer'}

    def authenticated(self, token):
        if not token or token not in self.sessions:
            fail(401, 'Authentication required')
        db = self.repo.read()
        customer = db['customers'].get(self.sessions[token])
        if not customer or not customer['active']:
            fail(403, 'Account deactivated')
        return customer

    def update_customer(self, customer_id, changes):
        with self.repo.lock:
            db = self.repo.read()
            customer = db['customers'][customer_id]
            customer.update(changes)
            self.repo.save(db)
            return safe_customer(customer)

    def deactivate(self, customer_id):
        with self.repo.lock:
            db = self.repo.read()
            db['customers'][customer_id]['active'] = False
            db['carts'].pop(customer_id, None)
            self.repo.save(db)

    def _item(self, item_id):
        item = self._lookup_item(item_id)
        if getattr(item, 'available', True) is False or getattr(item, 'active', True) is False:
            fail(409, 'Menu item unavailable')
        return item

    def _lookup_item(self, item_id):
        item = self.items.get_by_item_id(item_id)
        if not item:
            fail(404, 'Menu item not found')
        return item

    def _restaurant(self, restaurant_id):
        restaurant = self.restaurants.get_by_id(str(restaurant_id))
        if not restaurant:
            fail(404, 'Restaurant not found')
        if not restaurant.is_open:
            fail(409, 'Restaurant is closed')
        return restaurant

    def _view_cart(self, cart):
        lines = []
        subtotal = 0
        for item_id, quantity in cart.get('items', {}).items():
            item = self._lookup_item(item_id)
            unit = int(item.price)
            lines.append({'item_id': item_id, 'name': item.name, 'quantity': quantity,
                          'unit_price_cents': unit, 'line_total_cents': quantity * unit})
            subtotal += quantity * unit
        return {'restaurant_id': cart.get('restaurant_id'), 'items': lines,
                'subtotal_cents': subtotal, 'total_cents': subtotal}

    def cart(self, customer_id):
        db = self.repo.read()
        cart = db['carts'].get(customer_id, {'restaurant_id': None, 'items': {}})
        return self._view_cart(cart)

    def add(self, customer_id, item_id, quantity):
        if quantity < 1:
            fail(422, 'Quantity must be positive')
        with self.repo.lock:
            item = self._item(item_id)
            rid = str(item.restaurant_id)
            self._restaurant(rid)
            db = self.repo.read()
            cart = db['carts'].setdefault(customer_id, {'restaurant_id': rid, 'items': {}})
            if cart['restaurant_id'] not in (None, rid):
                fail(409, 'Cart must contain items from one restaurant')
            cart['restaurant_id'] = rid
            cart['items'][item_id] = cart['items'].get(item_id, 0) + quantity
            self.repo.save(db)
            return self._view_cart(cart)

    def change(self, customer_id, item_id, quantity):
        if quantity < 1:
            fail(422, 'Quantity must be positive; use DELETE to remove')
        with self.repo.lock:
            db = self.repo.read()
            cart = db['carts'].get(customer_id)
            if not cart or item_id not in cart['items']:
                fail(404, 'Item not in cart')
            item = self._item(item_id)
            self._restaurant(item.restaurant_id)
            cart['items'][item_id] = quantity
            self.repo.save(db)
            return self._view_cart(cart)

    def remove(self, customer_id, item_id):
        with self.repo.lock:
            db = self.repo.read()
            cart = db['carts'].get(customer_id)
            if not cart or item_id not in cart['items']:
                fail(404, 'Item not in cart')
            del cart['items'][item_id]
            if not cart['items']:
                cart['restaurant_id'] = None
            self.repo.save(db)
            return self._view_cart(cart)

    def clear(self, customer_id):
        with self.repo.lock:
            db = self.repo.read()
            db['carts'].pop(customer_id, None)
            self.repo.save(db)
            return {'restaurant_id': None, 'items': [], 'subtotal_cents': 0, 'total_cents': 0}

    def checkout(self, customer_id):
        with self.repo.lock:
            db = self.repo.read()
            customer = db['customers'].get(customer_id)
            if not customer or not customer['active'] or not customer['address']:
                fail(409, 'Active customer with address required')
            cart = db['carts'].get(customer_id)
            if not cart or not cart['items']:
                fail(409, 'Cart is empty')
            self._restaurant(cart['restaurant_id'])
            for item_id, qty in cart['items'].items():
                if qty < 1 or str(self._item(item_id).restaurant_id) != cart['restaurant_id']:
                    fail(409, 'Invalid cart contents')
            view = self._view_cart(cart) 
            order = {'id': str(uuid4()), 'customer_id': customer_id,
                     'restaurant_id': cart['restaurant_id'], 'delivery_address': customer['address'],
                     'items': view['items'], 'subtotal_cents': view['subtotal_cents'],
                     'total_cents': view['total_cents'], 'status': 'created',
                     'created_at': datetime.now(timezone.utc).isoformat()}
            db['orders'][order['id']] = order
            db['carts'].pop(customer_id, None)
            self.repo.save(db)
            return order

    def get_order(self, customer_id, order_id):
        order = self.repo.read()['orders'].get(order_id)
        if not order:
            fail(404, 'Order not found')
        if order['customer_id'] != customer_id:
            fail(403, 'Order belongs to another customer')
        return order

    def list_orders(self, customer_id):
        return [o for o in self.repo.read()['orders'].values() if o['customer_id'] == customer_id]
