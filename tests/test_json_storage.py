
import json

import pytest

from app.repositories import json_storage


def test_save_json_creates_file(tmp_path):
    path = tmp_path / "data.json"
    data = {"name": "Test", "price": 1299}

    json_storage.save_json(path, data)

    assert json.loads(path.read_text(encoding="utf-8")) == data


def test_save_json_replaces_existing_file(tmp_path):
    path = tmp_path / "data.json"

    json_storage.save_json(path, {"version": 1})
    json_storage.save_json(path, {"version": 2})

    assert json.loads(path.read_text(encoding="utf-8")) == {
        "version": 2
    }


def test_save_json_preserves_original_on_replace_failure(
    tmp_path, monkeypatch
):
    path = tmp_path / "data.json"
    json_storage.save_json(path, {"version": 1})

    def fail_replace(source, destination):
        raise OSError("Simulated replacement failure")

    monkeypatch.setattr(json_storage.os, "replace", fail_replace)

    with pytest.raises(OSError):
        json_storage.save_json(path, {"version": 2})

    assert json.loads(path.read_text(encoding="utf-8")) == {
        "version": 1
    }

    assert list(tmp_path.glob("*.tmp")) == []
