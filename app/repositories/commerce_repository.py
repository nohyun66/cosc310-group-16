import json
from pathlib import Path
from threading import RLock

from app.repositories.json_storage import save_json

_LOCK = RLock()

DEFAULT_FILE = Path(__file__).resolve().parents[2] / "data" / "commerce.json"


class CommerceRepository:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else DEFAULT_FILE
        self.lock = _LOCK

    def read(self):
        if not self.path.exists():
            return {
                "customers": {},
                "carts": {},
                "orders": {}
            }

        with self.path.open(encoding="utf-8") as file:
            result = json.load(file)

        for key in ("customers", "carts", "orders"):
            result.setdefault(key, {})

        return result

    def save(self, data):
        save_json(self.path, data)