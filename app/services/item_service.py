from app.schemas.item import Item
from app.repositories.item_repository import ItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from fastapi import HTTPException


class ItemService:
    def __init__(self):
        self.repository = ItemRepository()
        self.restaurant_repository = RestaurantRepository()

    def get_restaurant_menu(self, restaurant_id: str) -> list[Item]:
        """Return all menu items for a restaurant."""

        restaurant = self.restaurant_repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail=f"Restaurant ID: {restaurant_id} not found"
            )

        return self.repository.get_by_restaurant_id(restaurant_id)

    def get_menu_item(self, restaurant_id: str, item_id: str) -> Item:
        """Return a specific menu item from a restaurant."""

        restaurant = self.restaurant_repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail=f"Restaurant ID: {restaurant_id} not found"
            )

        item = self.repository.get_by_item_id(item_id)

        if item is None or str(item.restaurant_id) != restaurant_id:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item_id} not found"
            )

        return item