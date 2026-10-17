import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import restaurant_repository
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import RestaurantService


@pytest.fixture
def search_data(tmp_path, monkeypatch):
    # Use an existing valid record as a template for controlled test data.
    original_file = restaurant_repository.DATA_PATH

    with open(original_file, encoding="utf-8") as data_file:
        records = json.load(data_file)

    template = records[0]

    test_records = []

    for restaurant_id, name in [
        ("search-1", "Maple Pizza"),
        ("search-2", "River Grill"),
        ("search-3", "Pizza Corner"),
    ]:
        record = template.copy()
        record["id"] = restaurant_id
        record["name"] = name
        test_records.append(record)

    # Write only to a temporary file.
    test_file = tmp_path / "restaurants.json"

    with open(test_file, "w", encoding="utf-8") as data_file:
        json.dump(test_records, data_file)

    monkeypatch.setattr(restaurant_repository, "DATA_PATH", test_file)

    return test_file


def test_search_returns_partial_matches(search_data):
    # Only names containing "pizza" should be returned.
    response = TestClient(app).get(
        "/restaurants",
        params={"search": "pizza"},
    )

    assert response.status_code == 200

    names = []
    for restaurant in response.json():
        names.append(restaurant["name"])

    assert names == ["Maple Pizza", "Pizza Corner"]


def test_search_ignores_capitalization(search_data):
    # Uppercase search text should match mixed-case names.
    response = TestClient(app).get(
        "/restaurants",
        params={"search": "RIVER"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "River Grill"


def test_search_without_matches_returns_empty_list(search_data):
    response = TestClient(app).get(
        "/restaurants",
        params={"search": "no-such-name"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_without_search_returns_all_restaurants(search_data):
    response = TestClient(app).get("/restaurants")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_empty_data_returns_empty_list(search_data):
    # Empty the temporary file, leaving project data unchanged.
    search_data.write_text("[]", encoding="utf-8")

    response = TestClient(app).get("/restaurants")

    assert response.status_code == 200
    assert response.json() == []


def test_service_filters_names(search_data, monkeypatch):
    # Supply records directly so this unit test checks the service logic.
    restaurants = RestaurantRepository().get_all_restaurants()
    service = RestaurantService()

    monkeypatch.setattr(
        service.repository,
        "get_all_restaurants",
        lambda: restaurants,
    )

    matches = service.search_restaurants("PIZZA")

    assert len(matches) == 2
    assert matches[0].name == "Maple Pizza"
    assert matches[1].name == "Pizza Corner"