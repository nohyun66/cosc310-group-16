import shutil

import pytest

from app.repositories import restaurant_repository, item_repository

@pytest.fixture
def isolated_restaurants(tmp_path, monkeypatch):
    test_file = tmp_path / "restaurants.json"

    shutil.copyfile(
        restaurant_repository.DATA_PATH,
        test_file
    )

    monkeypatch.setattr(
        restaurant_repository,
        "DATA_PATH",
        test_file
    )


from app.main import app
from app.core.auth import current_user


@pytest.fixture
def admin_client():
    test_admin = {
        "id": "test-admin",
        "role": "admin",
        "active": True,
    }

    previous_override = app.dependency_overrides.get(current_user)
    app.dependency_overrides[current_user] = lambda: test_admin

    try:
        from fastapi.testclient import TestClient
        yield TestClient(app)
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(current_user, None)
        else:
            app.dependency_overrides[current_user] = previous_override

@pytest.fixture
def isolated_items(tmp_path, monkeypatch):
    test_file = tmp_path / "items.json"
    shutil.copyfile(item_repository.DATA_PATH, test_file)
    monkeypatch.setattr(item_repository, "DATA_PATH", test_file)


