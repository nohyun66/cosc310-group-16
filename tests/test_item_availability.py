import shutil

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import item_repository, restaurant_repository
from app.repositories.item_repository import ItemRepository
from app.services.item_service import ItemService


@pytest.fixture
def isolated_data(tmp_path, monkeypatch):
    # use temporary copies of both files.
    restaurant_file = tmp_path / "restaurants.json"
    item_file = tmp_path / "items.json"

    shutil.copyfile(restaurant_repository.DATA_PATH, restaurant_file)
    shutil.copyfile(item_repository.DATA_PATH, item_file)

    monkeypatch.setattr(
        restaurant_repository, "DATA_PATH", restaurant_file
    )
    monkeypatch.setattr(item_repository, "DATA_PATH", item_file)


def test_existing_items_default_to_active_and_available(isolated_data):
    # older records have no status fields and should still load.
    item = ItemRepository().get_by_item_id("R1-beef-pie")

    assert item is not None
    assert item.is_active is True
    assert item.is_available is True


@pytest.mark.parametrize(
    "available, active",
    [(False, True), (True, False), (True, True)],
)
def test_status_update_is_saved(isolated_data, available, active):
    # change status through the API and read it back from storage.
    client = TestClient(app)
    before = client.get(
        "/restaurants/1/menu/R1-beef-pie"
    ).json()

    response = client.patch(
        "/restaurants/1/menu/R1-beef-pie/status",
        json={"is_available": available, "is_active": active},
    )

    assert response.status_code == 200

    expected = before.copy()
    expected["is_available"] = available
    expected["is_active"] = active

    assert response.json() == expected

    saved = ItemRepository().get_by_item_id("R1-beef-pie")

    assert saved is not None
    assert saved.model_dump(mode="json") == expected


@pytest.mark.parametrize(
    "restaurant_id, item_id",
    [
        ("does-not-exist", "R1-beef-pie"),
        ("1", "does-not-exist"),
        ("2", "R1-beef-pie"),
    ],
)
def test_invalid_status_target_leaves_data_unchanged(
    isolated_data, restaurant_id, item_id
):
    # missing records and wrong restaurant ownership must not write data.
    before = item_repository.DATA_PATH.read_bytes()

    response = TestClient(app).patch(
        f"/restaurants/{restaurant_id}/menu/{item_id}/status",
        json={"is_available": False, "is_active": False},
    )

    assert response.status_code == 404
    assert item_repository.DATA_PATH.read_bytes() == before


@pytest.mark.parametrize(
    "available, active, message",
    [
        (False, True, "Menu item is unavailable"),
        (True, False, "Menu item is deactivated"),
    ],
)
def test_unorderable_item_is_rejected(
    isolated_data, available, active, message
):
    # the shared eligibility method rejects items that cannot be purchased.
    service = ItemService()
    service.update_menu_item_status(
        "1", "R1-beef-pie", available, active
    )

    with pytest.raises(HTTPException) as error:
        service.get_orderable_menu_item("1", "R1-beef-pie")

    assert error.value.status_code == 409
    assert error.value.detail == message


def test_available_item_is_orderable(isolated_data):
    service = ItemService()

    item = service.get_orderable_menu_item("1", "R1-beef-pie")

    assert item.id == "R1-beef-pie"


def test_editing_details_preserves_status(isolated_data):
    # editing details must not reactivate an item.
    client = TestClient(app)

    response = client.patch(
        "/restaurants/1/menu/R1-beef-pie/status",
        json={"is_available": False, "is_active": False},
    )
    assert response.status_code == 200

    details = {
        "name": "Updated Beef Pie",
        "cuisine": "NORAM",
        "category": "Main",
        "price": 1399,
        "description": "Updated description",
        "image_url": "https://example.com/beef-pie.jpg",
    }

    response = client.put(
        "/restaurants/1/menu/R1-beef-pie",
        json=details,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Beef Pie"

    saved = ItemRepository().get_by_item_id("R1-beef-pie")

    assert saved is not None
    assert saved.price == 1399
    assert saved.is_available is False
    assert saved.is_active is False