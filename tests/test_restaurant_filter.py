import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import restaurant_repository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cuisine import Cuisine
from app.services.restaurant_service import RestaurantService


@pytest.fixture
def filter_data(tmp_path, monkeypatch):
    # Use a valid restaurant record as the template.
    with open(
        restaurant_repository.DATA_PATH,
        encoding="utf-8",
    ) as data_file:
        records = json.load(data_file)

    template = records[0]
    test_records = []

    for restaurant_id, cuisine in [
        ("filter-1", "ASIAN"),
        ("filter-2", "MED"),
        ("filter-3", "ASIAN"),
    ]:
        record = template.copy()
        record["id"] = restaurant_id
        record["cuisine"] = cuisine
        test_records.append(record)

    # Store controlled test records in a temporary file.
    test_file = tmp_path / "restaurants.json"

    with open(test_file, "w", encoding="utf-8") as data_file:
        json.dump(test_records, data_file)

    monkeypatch.setattr(restaurant_repository, "DATA_PATH", test_file)


def test_filter_returns_selected_cuisine(filter_data):
    # Return both ASIAN restaurants and exclude the MED restaurant.
    response = TestClient(app).get(
        "/restaurants",
        params={"cuisine": "ASIAN"},
    )

    assert response.status_code == 200

    restaurant_ids = []

    for restaurant in response.json():
        restaurant_ids.append(restaurant["id"])
        assert restaurant["cuisine"] == "ASIAN"

    assert restaurant_ids == ["filter-1", "filter-3"]


def test_filter_without_matches_returns_empty_list(filter_data):
    # EURO is supported, but no test restaurant has that cuisine.
    response = TestClient(app).get(
        "/restaurants",
        params={"cuisine": "EURO"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_unsupported_cuisine_returns_validation_error(filter_data):
    response = TestClient(app).get(
        "/restaurants",
        params={"cuisine": "UNKNOWN"},
    )

    assert response.status_code == 422


def test_without_filter_returns_all_restaurants(filter_data):
    response = TestClient(app).get("/restaurants")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_service_filters_cuisine(filter_data, monkeypatch):
    # Test service filtering separately from the HTTP endpoint.
    restaurants = RestaurantRepository().get_all_restaurants()
    service = RestaurantService()

    monkeypatch.setattr(
        service.repository,
        "get_all_restaurants",
        lambda: restaurants,
    )

    matches = service.get_all_restaurants(Cuisine.MED)

    assert len(matches) == 1
    assert matches[0].id == "filter-2"