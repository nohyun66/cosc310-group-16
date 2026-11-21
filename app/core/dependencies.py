from app.services.commerce_service import CommerceService

# login and protected requests must share the same session store.
commerce_service = CommerceService()