import hashlib
import hmac
import secrets
from uuid import uuid4
from app.services.util import fail
from app.repositories.commerce_repository import CommerceRepository
from app.services.customer_service import safe_customer

class AuthService:
    def __init__(self, repo=None):
        self.repo = repo or CommerceRepository()
        self.sessions = {}

    def register(self, data):
        with self.repo.lock:
            db = self.repo.read()
            email = str(data.email).lower()
            if any(c["email"] == email for c in db["customers"].values()):
                fail(409, 'Email already registered')
            salt = secrets.token_hex(16)
            hashed = hashlib.pbkdf2_hmac(
                "sha256", data.password.encode(), bytes.fromhex(salt), 200_000
            ).hex()
            customer = {
                "id": str(uuid4()),
                "email": email,
                "name": data.name,
                "address": data.address,
                "active": True,
                "role": "customer",
                "salt": salt,
                "password_hash": hashed,
            }
            db["customers"][customer["id"]] = customer
            self.repo.save(db)
            return safe_customer(customer)

    def login(self, email, password):
        with self.repo.lock:
            customers = self.repo.read()["customers"].values()
            customer = next((c for c in customers if c["email"] == email.lower()), None)
            if not customer or not customer["active"]:
                fail(401, 'Invalid credentials')
            proposed = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), bytes.fromhex(customer["salt"]), 200_000
            ).hex()
            if not hmac.compare_digest(proposed, customer["password_hash"]):
                fail(401, 'Invalid credentials')
            token = secrets.token_urlsafe(32)
            self.sessions[token] = customer["id"]
            return {"access_token": token, "token_type": "bearer"}

    def authenticated(self, token):
        if not token or token not in self.sessions:
            fail(401, "Authentication required")
        db = self.repo.read()
        customer = db["customers"].get(self.sessions[token])
        if not customer or not customer["active"]:
            fail(403, "Account deactivated")
        return customer
