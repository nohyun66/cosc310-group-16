import shutil

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import item_repository, restaurant_repository
from app.repositories.item_repository import ItemRepository
from app.repositories.restaurant_repository import RestaurantRepository


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


def test_health_endpoint():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


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


def test_create_menu_item(isolated_items):
    new_item = {
        "name": "Test Item",
        "cuisine": "ASIAN",
        "category": "Main",
        "price": 999,
        "description": "Test description",
        "image_url": "https://example.com/test-item.jpg",
    }

    response = TestClient(app).post("/restaurants/1/menu", json=new_item)

    assert response.status_code == 201
    assert response.json()["id"] == "R1-test-item"
    assert response.json()["restaurant_id"] == 1

    saved = ItemRepository().get_by_item_id("R1-test-item")
    assert saved is not None
    assert saved.name == "Test Item"


def test_create_menu_item_rejects_invalid_cuisine(isolated_items):
    new_item = {
        "name": "Test Item",
        "cuisine": "INVALID",
        "category": "Main",
        "price": 999,
    }

    response = TestClient(app).post("/restaurants/1/menu", json=new_item)

    assert response.status_code == 422


def test_update_menu_item(isolated_items):
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
    )

    assert response.status_code == 200
    assert response.json()["id"] == "R1-beef-pie"
    assert response.json()["name"] == "Updated Beef Pie"
    assert response.json()["price"] == 1399

    saved = ItemRepository().get_by_item_id("R1-beef-pie")
    assert saved is not None
    assert saved.description == "Updated description"


def test_update_menu_item_returns_404_for_missing_item(isolated_items):
    updated_data = {
        "name": "Unknown Item",
        "cuisine": "NORAM",
        "category": "Main",
        "price": 999,
    }

    response = TestClient(app).put(
        "/restaurants/1/menu/does-not-exist",
        json=updated_data,
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

def test_create_restaurant(isolated_restaurants):
    new_restaurant = {
        "name": "Korean BBQ",
        "cuisine": "ASIAN",
        "description": "Korean BBQ restaurant",
        "image_url": "https://example.com/korean-bbq.jpg",
        "is_open": True,
        "rating": 4.5
    }

    response = TestClient(app).post("/restaurants", json=new_restaurant)

    assert response.status_code == 201
    assert response.json()["name"] == "Korean BBQ"

    restaurant_id = response.json()["id"]
    saved = RestaurantRepository().get_by_id(restaurant_id)

    assert saved is not None
    assert saved.name == "Korean BBQ"

def test_update_restaurant(isolated_restaurants):
    updated_data = {
        "name": "Updated Korean BBQ",
        "cuisine": "ASIAN",
        "description": "Updated restaurant description",
        "image_url": "https://example.com/korean-bbq.jpg",
        "is_open": True,
        "rating": 4.8
    }

    response = TestClient(app).put("/restaurants/1", json=updated_data)

    assert response.status_code == 200
    assert response.json()["id"] == "1"
    assert response.json()["name"] == "Updated Korean BBQ"

    saved = RestaurantRepository().get_by_id("1")

    assert saved is not None
    assert saved.name == "Updated Korean BBQ"
