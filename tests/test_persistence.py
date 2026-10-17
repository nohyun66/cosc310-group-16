import json
import shutil

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import restaurant_repository, item_repository
from app.repositories.item_repository import ItemRepository


@pytest.fixture
def isolated_data(tmp_path, monkeypatch):
    # Use temporary copies of both data files.
    restaurant_file = tmp_path / "restaurants.json"
    item_file = tmp_path / "items.json"

    shutil.copyfile(restaurant_repository.DATA_PATH, restaurant_file)
    shutil.copyfile(item_repository.DATA_PATH, item_file)

    monkeypatch.setattr(
        restaurant_repository, "DATA_PATH", restaurant_file
    )
    monkeypatch.setattr(
        item_repository, "DATA_PATH", item_file
    )

    return restaurant_file


def read_saved_restaurant(data_file, restaurant_id):
    # Read the JSON file directly to check what was saved.
    with open(data_file, encoding="utf-8") as file:
        restaurants = json.load(file)

    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant

    return None


def test_restaurant_changes_are_saved(isolated_data):
    client = TestClient(app)

    details = {
        "name": "Test Restaurant",
        "cuisine": "ASIAN",
        "description": "Restaurant for testing",
        "image_url": "https://example.com/restaurant.jpg",
        "is_open": True,
        "rating": 4.0,
    }

    # Create a restaurant and check the saved file.
    response = client.post("/restaurants", json=details)

    assert response.status_code == 201
    created = response.json()
    restaurant_id = created["id"]

    saved = read_saved_restaurant(isolated_data, restaurant_id)
    assert saved == created

    # Update it and check that the same ID has the new details.
    details["name"] = "Updated Restaurant"

    response = client.put(
        f"/restaurants/{restaurant_id}",
        json=details,
    )

    assert response.status_code == 200
    assert response.json()["id"] == restaurant_id

    saved = read_saved_restaurant(isolated_data, restaurant_id)
    assert saved == response.json()
    assert saved["name"] == "Updated Restaurant"


def test_restaurant_update_preserves_menu(isolated_data):
    client = TestClient(app)

    # Find a restaurant that has a menu item.
    items_before = ItemRepository().get_all_items()
    assert items_before
    restaurant_id = str(items_before[0].restaurant_id)

    response = client.get(f"/restaurants/{restaurant_id}/menu")
    assert response.status_code == 200
    menu_before = response.json()
    assert menu_before

    # Get the restaurant details and change its name.
    response = client.get(f"/restaurants/{restaurant_id}")
    assert response.status_code == 200

    details = response.json()
    del details["id"]
    details["name"] = "Updated Restaurant"

    response = client.put(
        f"/restaurants/{restaurant_id}",
        json=details,
    )

    assert response.status_code == 200
    assert response.json()["id"] == restaurant_id

    # The menu and all stored menu items must remain unchanged.
    response = client.get(f"/restaurants/{restaurant_id}/menu")

    assert response.status_code == 200
    assert response.json() == menu_before
    assert ItemRepository().get_all_items() == items_before