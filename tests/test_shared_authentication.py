from fastapi.testclient import TestClient

from app.main import app
from app.repositories.commerce_repository import CommerceRepository
from app.services.commerce_services import (
    auth_service,
    cart_service,
    customer_service,
    order_service,
)


def test_shared_login_across_commerce_and_admin_routes(
    tmp_path, monkeypatch, isolated_items
):
    repository = CommerceRepository(tmp_path / "commerce.json")

    for service in (
        auth_service,
        customer_service,
        cart_service,
        order_service,
    ):
        monkeypatch.setattr(service, "repo", repository)

    monkeypatch.setattr(auth_service, "sessions", {})

    client = TestClient(app)

    response = client.post(
        "/customers/register",
        json={
            "name": "Shared Auth Test",
            "email": "shared@example.com",
            "password": "TestPassword123!",
            "address": "123 Test Street",
        },
    )
    assert response.status_code == 201
    customer_id = response.json()["id"]

    response = client.post(
        "/customers/login",
        json={
            "email": "shared@example.com",
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 200

    headers = {
        "Authorization": f"Bearer {response.json()['access_token']}"
    }

    response = client.get("/customers/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == customer_id

    response = client.get("/restaurants/1/menu/R1-beef-pie")
    assert response.status_code == 200
    item = response.json()

    response = client.post(
        "/cart/items",
        headers=headers,
        json={"item_id": item["id"], "quantity": 1},
    )
    assert response.status_code == 200
    assert response.json()["total_cents"] == item["price"]

    details = {
        key: item[key]
        for key in (
            "name",
            "cuisine",
            "category",
            "price",
            "description",
            "image_url",
        )
    }

    # A customer cannot perform an admin operation.
    response = client.put(
        "/restaurants/1/menu/R1-beef-pie",
        headers=headers,
        json=details,
    )
    assert response.status_code == 403

    # Change the role only in temporary test storage.
    data = repository.read()
    data["customers"][customer_id]["role"] = "admin"
    repository.save(data)

    # The same token is recognized by the admin check.
    response = client.put(
        "/restaurants/1/menu/R1-beef-pie",
        headers=headers,
        json=details,
    )
    assert response.status_code == 200

    response = client.post("/checkout", headers=headers)
    assert response.status_code == 201
    assert response.json()["customer_id"] == customer_id

    response = client.get("/cart", headers=headers)
    assert response.status_code == 200
    assert response.json()["items"] == []