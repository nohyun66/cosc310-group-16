import json
from pathlib import Path

from app.schemas.item import Item, ItemCreate

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "items.json"


class ItemRepository:
    """Read menu items from the JSON data store."""

    def get_all_items(self) -> list[Item]:
        """Return all menu items."""
        with open(DATA_PATH, encoding="utf-8") as data_file:
            data = json.load(data_file)

        items = []
        for item in data:
            items.append(Item(**item))

        return items

    def get_by_restaurant_id(self, restaurant_id: str) -> list[Item]:
        """Return all menu items for a specific restaurant."""
        items = self.get_all_items()
        restaurant_items = []

        for item in items:
            if str(item.restaurant_id) == restaurant_id:
                restaurant_items.append(item)

        return restaurant_items

    def get_by_item_id(self, item_id: str) -> Item | None:
        for item in self.get_all_items():
            if item.id == item_id:
                return item
        return None

    def create_item(self, restaurant_id: str, item_name: str, new_item: ItemCreate) -> Item | None:
        item_id = "R" + restaurant_id + "-" + item_name.lower()
        items = self.get_all_items()

        new_Item = Item(id=item_id,
                    restaurant_id=restaurant_id
                    **new_item.model_dump()
                )

        with open(DATA_PATH, "w", encoding="utf-8") as data_file:
                    json.dump(
                        [item.model_dump(mode="json") for item in items],
                        data_file,
                        indent=2
                    )
        
        return new_Item