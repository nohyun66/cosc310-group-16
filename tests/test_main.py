import shutil

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import restaurant_repository
from app.repositories.restaurant_repository import RestaurantRepository


@pytest.fixture
def isolated_restaurants(tmp_path, monkeypatch):
    # each test gets own copy of restaurant data 
    test_file = tmp_path / "restaurants.json"
    # copies the data, then the repository reads the copy 
    shutil.copyfile(restaurant_repository.DATA_PATH, test_file)
    monkeypatch.setattr(restaurant_repository, "DATA_PATH", test_file)


def test_health_endpoint():
    # health confirms the app is running 
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_restaurant_list_endpoint(isolated_restaurants):
    response = TestClient(app).get("/restaurants")
    # restaurant endpoint returns at least two restaurants
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_repository_reads_isolated_data(isolated_restaurants):
    # find a restaurant in the temporary data file 
    repository = RestaurantRepository()
    restaurants = repository.get_all_restaurants()
    first_restaurant = restaurants[0]

    found_restaurant = repository.get_by_id(first_restaurant.id)

    assert found_restaurant is not None
    assert found_restaurant.id == first_restaurant.id


def test_missing_restaurant_returns_404(isolated_restaurants):
    # request an ID that does not exist should give us 404
    response = TestClient(app).get("/restaurants/does-not-exist")

    assert response.status_code == 404