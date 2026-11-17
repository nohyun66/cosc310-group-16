import shutil

import pytest

import json
import jwt

from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

from app.core import config

from app.main import app
from app.repositories import item_repository, restaurant_repository, customer_repository
from app.repositories.item_repository import ItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.customer_repository import CustomerRepository
from app.services.customer_service import password_hash


@pytest.fixture
def isolated_restaurants(tmp_path, monkeypatch):
    test_file = tmp_path / "restaurants.json"
    shutil.copyfile(restaurant_repository.DATA_PATH, test_file)
    monkeypatch.setattr(restaurant_repository, "DATA_PATH", test_file)


@pytest.fixture
def isolated_items(tmp_path, monkeypatch):
    test_file = tmp_path / "items.json"
    shutil.copyfile(item_repository.DATA_PATH, test_file)
    monkeypatch.setattr(item_repository, "DATA_PATH", test_file)

@pytest.fixture
def isolated_customers(tmp_path, monkeypatch):
    test_file = tmp_path / "customers.json"
    test_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(customer_repository, "DATA_PATH", test_file)
    return test_file

@pytest.fixture
def registration_details():
    return {
        "name": "Demo Customer",
        "email": "demo@example.com",
        "password": "DemoPassword123!",
        "delivery_address": "123 Demo Street",
    }

@pytest.fixture
def auth_customer(isolated_customers, registration_details, monkeypatch):
    # use a test-only key, independent of terminal configuration.
    monkeypatch.setattr(config, "JWT_SECRET_KEY", "test-only-signing-key-" * 3)

    response = TestClient(app).post(
        "/customers", json=registration_details
    )
    assert response.status_code == 201

    return response.json()

@pytest.fixture
def admin_headers(auth_customer, registration_details, isolated_customers):
    records = json.loads(
        isolated_customers.read_text(encoding="utf-8")
    )
    records[0]["role"] = "admin"
    isolated_customers.write_text(
        json.dumps(records), encoding="utf-8"
    )

    response = TestClient(app).post(
        "/auth/login",
        json={
            "email": registration_details["email"],
            "password": registration_details["password"],
        },
    )
    assert response.status_code == 200

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.parametrize(
    "method, path",
    [
        ("POST", "/restaurants"),
        ("PUT", "/restaurants/1"),
        ("POST", "/restaurants/1/menu"),
        ("PUT", "/restaurants/1/menu/R1-beef-pie"),
    ],
)

def test_management_rejects_customer_role(
    auth_customer,
    registration_details,
    isolated_restaurants,
    isolated_items,
    method,
    path,
):
    client = TestClient(app)

    response = client.post(
        "/auth/login",
        json={
            "email": registration_details["email"],
            "password": registration_details["password"],
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    restaurants_before = restaurant_repository.DATA_PATH.read_bytes()
    items_before = item_repository.DATA_PATH.read_bytes()

    response = client.request(
        method,
        path,
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert restaurant_repository.DATA_PATH.read_bytes() == restaurants_before
    assert item_repository.DATA_PATH.read_bytes() == items_before


@pytest.mark.parametrize(
    "method, path",
    [
        ("POST", "/restaurants"),
        ("PUT", "/restaurants/1"),
        ("POST", "/restaurants/1/menu"),
        ("PUT", "/restaurants/1/menu/R1-beef-pie"),
    ],
)
def test_management_requires_authentication(method, path):
    response = TestClient(app).request(method, path, json={})

    assert response.status_code == 401


def test_health_endpoint():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_frontend_page_is_served():
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert 'id="restaurants"' in response.text
    assert 'name="search"' in response.text
    assert 'name="cuisine"' in response.text
    assert "params.set(\"search\", search)" in response.text
    assert "params.set(\"cuisine\", cuisine)" in response.text
    assert "restaurant.html?id=" in response.text


def test_restaurant_details_page_is_served():
    response = TestClient(app).get("/restaurant.html")

    assert response.status_code == 200
    assert 'id="restaurant-description"' in response.text
    assert 'id="restaurant-image"' in response.text
    assert 'id="restaurant-open"' in response.text
    assert 'fetch(`/restaurants/${encodeURIComponent(restaurantId)}/menu`)' in response.text
    assert "restaurant.html?id=" in response.text


def test_restaurant_details_page_is_served():
    response = TestClient(app).get("/restaurant.html")

    assert response.status_code == 200
    assert 'id="restaurant-description"' in response.text
    assert 'id="menu"' in response.text


def test_restaurant_list_endpoint(isolated_restaurants):
    response = TestClient(app).get("/restaurants")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_repository_reads_isolated_data(isolated_restaurants):
    repository = RestaurantRepository()
    restaurants = repository.get_all_restaurants()
    first_restaurant = restaurants[0]

    found_restaurant = repository.get_by_id(first_restaurant.id)

    assert found_restaurant is not None
    assert found_restaurant.id == first_restaurant.id


def test_missing_restaurant_returns_404(isolated_restaurants):
    response = TestClient(app).get("/restaurants/does-not-exist")

    assert response.status_code == 404
def test_restaurant_menu(isolated_restaurants):
    response = TestClient(app).get("/restaurants/1/menu")

    assert response.status_code == 200
    assert len(response.json()) == 9
    assert response.json()[0]["name"] == "Beef pie"

def test_get_menu_item(isolated_restaurants):
    response = TestClient(app).get("/restaurants/1/menu/R1-beef-pie")

    assert response.status_code == 200
    assert response.json()["id"] == "R1-beef-pie"
    assert response.json()["name"] == "Beef pie"
    assert response.json()["price"] == 1299

def test_missing_menu_item_returns_404(isolated_restaurants):
    response = TestClient(app).get("/restaurants/1/menu/does-not-exist")

    assert response.status_code == 404


def test_create_menu_item(isolated_items, admin_headers):
    new_item = {
        "name": "Test Item",
        "cuisine": "ASIAN",
        "category": "Main",
        "price": 999,
        "description": "Test description",
        "image_url": "https://example.com/test-item.jpg",
    }
    response = TestClient(app).post(
        "/restaurants/1/menu",
        json=new_item,
        headers=admin_headers,
)


def test_create_menu_item_rejects_invalid_cuisine(isolated_items, admin_headers):
    new_item = {
        "name": "Test Item",
        "cuisine": "INVALID",
        "category": "Main",
        "price": 999,
    }

    response = TestClient(app).post(
        "/restaurants/1/menu",
        json=new_item,
        headers=admin_headers,
)

    assert response.status_code == 422


def test_update_menu_item(isolated_items, admin_headers):
    updated_data = {
        "name": "Updated Beef Pie",
        "cuisine": "NORAM",
        "category": "Main",
        "price": 1399,
        "description": "Updated description",
        "image_url": "https://example.com/updated-beef-pie.jpg",
    }

    response = TestClient(app).put(
        "/restaurants/1/menu/R1-beef-pie",
        json=updated_data,
        headers=admin_headers,
)

    assert response.status_code == 200
    assert response.json()["id"] == "R1-beef-pie"
    assert response.json()["name"] == "Updated Beef Pie"
    assert response.json()["price"] == 1399

    saved = ItemRepository().get_by_item_id("R1-beef-pie")
    assert saved is not None
    assert saved.description == "Updated description"


def test_update_menu_item_returns_404_for_missing_item(isolated_items, admin_headers):
    updated_data = {
        "name": "Unknown Item",
        "cuisine": "NORAM",
        "category": "Main",
        "price": 999,
    }

    response = TestClient(app).put(
        "/restaurants/1/menu/does-not-exist",
        json=updated_data,
        headers=admin_headers,
)

    assert response.status_code == 404


def test_restaurant_search(isolated_restaurants):
    response = TestClient(app).get("/restaurants?search=Asian")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Asian Restaurant"


def test_restaurant_cuisine_filter(isolated_restaurants):
    response = TestClient(app).get("/restaurants?cuisine=ASIAN")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["cuisine"] == "ASIAN"

def test_create_restaurant(isolated_restaurants, admin_headers):
    new_restaurant = {
        "name": "Korean BBQ",
        "cuisine": "ASIAN",
        "description": "Korean BBQ restaurant",
        "image_url": "https://example.com/korean-bbq.jpg",
        "is_open": True,
        "rating": 4.5
    }

    response = TestClient(app).post(
        "/restaurants",
        json=new_restaurant,
        headers=admin_headers,
)

    assert response.status_code == 201
    assert response.json()["name"] == "Korean BBQ"

    restaurant_id = response.json()["id"]
    saved = RestaurantRepository().get_by_id(restaurant_id)

    assert saved is not None
    assert saved.name == "Korean BBQ"

def test_update_restaurant(isolated_restaurants, admin_headers):
    updated_data = {
        "name": "Updated Korean BBQ",
        "cuisine": "ASIAN",
        "description": "Updated restaurant description",
        "image_url": "https://example.com/korean-bbq.jpg",
        "is_open": True,
        "rating": 4.8
    }

    response = TestClient(app).put(
        "/restaurants/1",
        json=updated_data,
        headers=admin_headers,
)

    assert response.status_code == 200
    assert response.json()["id"] == "1"
    assert response.json()["name"] == "Updated Korean BBQ"

    saved = RestaurantRepository().get_by_id("1")

    assert saved is not None
    assert saved.name == "Updated Korean BBQ"

def test_registration_saves_customer(
    isolated_customers, registration_details
):
    response = TestClient(app).post(
        "/customers", json=registration_details
    )

    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "Demo Customer"
    assert result["role"] == "customer"
    assert result["is_active"] is True
    assert "password" not in result
    assert "password_hash" not in result

    saved = CustomerRepository().get_by_id(result["id"])

    assert saved is not None
    assert saved.email == "demo@example.com"
    assert saved.password_hash != registration_details["password"]
    assert password_hash.verify(
        registration_details["password"], saved.password_hash
    )
    assert registration_details["password"] not in (
        isolated_customers.read_text(encoding="utf-8")
    )


def test_duplicate_email_does_not_change_storage(
    isolated_customers, registration_details
):
    client = TestClient(app)
    response = client.post("/customers", json=registration_details)
    assert response.status_code == 201

    before = isolated_customers.read_bytes()
    registration_details["email"] = " DEMO@EXAMPLE.COM "

    response = client.post("/customers", json=registration_details)

    assert response.status_code == 409
    assert isolated_customers.read_bytes() == before


def test_short_password_is_rejected(
    isolated_customers, registration_details
):
    registration_details["password"] = "short"

    response = TestClient(app).post(
        "/customers", json=registration_details
    )

    assert response.status_code == 422
    assert CustomerRepository().get_all_customers() == []


def test_registration_cannot_choose_admin_role(
    isolated_customers, registration_details
):
    registration_details["role"] = "admin"

    response = TestClient(app).post(
        "/customers", json=registration_details
    )

    assert response.status_code == 201
    assert response.json()["role"] == "customer"

    saved = CustomerRepository().get_by_id(response.json()["id"])
    assert saved is not None
    assert saved.role == "customer"



def test_login_and_get_current_customer(
    auth_customer, registration_details
):
    client = TestClient(app)

    response = client.post(
        "/auth/login",
        json={
            "email": registration_details["email"],
            "password": registration_details["password"],
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    token = response.json()["access_token"]
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == auth_customer
    assert "password_hash" not in response.json()


@pytest.mark.parametrize(
    "email, password",
    [
        ("demo@example.com", "wrong-password"),
        ("unknown@example.com", "DemoPassword123!"),
    ],
)
def test_login_rejects_incorrect_credentials(
    auth_customer, email, password
):
    response = TestClient(app).post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.parametrize("token", [None, "invalid-token"])
def test_current_customer_requires_valid_token(auth_customer, token):
    headers = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"

    response = TestClient(app).get("/auth/me", headers=headers)

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_expired_token_is_rejected(auth_customer):
    token = jwt.encode(
        {
            "sub": auth_customer["id"],
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )

    response = TestClient(app).get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_deactivation_blocks_login_and_existing_token(
    auth_customer, registration_details, isolated_customers
):
    client = TestClient(app)
    response = client.post(
        "/auth/login",
        json={
            "email": registration_details["email"],
            "password": registration_details["password"],
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Simulate account deactivation in temporary storage.
    records = json.loads(isolated_customers.read_text(encoding="utf-8"))
    records[0]["is_active"] = False
    isolated_customers.write_text(json.dumps(records), encoding="utf-8")

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403

    response = client.post(
        "/auth/login",
        json={
            "email": registration_details["email"],
            "password": registration_details["password"],
        },
    )
    assert response.status_code == 403    