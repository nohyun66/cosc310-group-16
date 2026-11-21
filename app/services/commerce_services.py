from app.repositories.commerce_repository import CommerceRepository
from app.services.auth_service import AuthService
from app.services.cart_service import CartService
from app.services.customer_service import CustomerService
from app.services.order_service import OrderService

commerce_repository = CommerceRepository()

auth_service = AuthService(repo=commerce_repository)
customer_service = CustomerService(repo=commerce_repository)
cart_service = CartService(repo=commerce_repository)
order_service = OrderService(repo=commerce_repository)
