from app.schemas.item import Item, ItemCategory
from app.repositories.item_repository import ItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cuisine import Cuisine
from fastapi import HTTPException
from pydantic import HttpUrl


class ItemService:
    def __init__(self):
        self.repository = ItemRepository()
        self.restaurant_repository = RestaurantRepository()

    def get_restaurant_menu(self, restaurant_id: int) -> list[Item]:
        """Return all menu items for a restaurant."""

        restaurant = self.restaurant_repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail=f"Restaurant ID: {restaurant_id} not found"
            )

        return self.repository.get_by_restaurant_id(restaurant_id)

    def get_menu_item(self, restaurant_id: int, item_id: str) -> Item:
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

    def validate_menu_item(self, item: Item) -> None:
        if self.restaurant_repository.get_by_id(item.restaurant_id) is None:
            raise HTTPException(
                status_code=404,
                detail=f"Restaurant ID: {item.restaurant_id} not found")
        
        if item.price <= 0:
            raise HTTPException(
                status_code=422,
                detail=f"Price: ({item.price}) must be greater than 0")

        return None
        

    def create_menu_item(self, restaurant_id: int, name: str, cuisine: Cuisine, 
                         category: ItemCategory, price: int, 
                         description: str = "Placeholder description", 
                         image_url: HttpUrl = "https://imgur.com/a/LCCoa9Z") -> Item:

        items = self.repository.get_all_items()
        new_item_id = f"R{restaurant_id}-{name.lower().replace(' ', '-')}"
        for item in items:
            if item.id == new_item_id:
                raise HTTPException(
                    status_code=409,
                    detail=f"Item ID: {new_item_id} already exists")        
        
        new_item = Item(id=new_item_id, restaurant_id=restaurant_id, name=name, 
                              cuisine=cuisine, category=category, price=price,
                              description=description, image_url=image_url)

        self.validate_menu_item(new_item)
        return self.repository.create_item(new_item)

    def update_menu_item(self, item_id: str, restaurant_id: int, name: str, cuisine: Cuisine, 
                         category: ItemCategory, price: int, 
                         description: str = "Placeholder description", 
                         image_url: HttpUrl = "https://imgur.com/a/LCCoa9Z") -> Item:
        item = self.get_menu_item(restaurant_id, item_id)

        new_item = Item(
            id=item.id,
            restaurant_id=item.restaurant_id,
            name=name,
            cuisine=cuisine,
            category=category,
            price=price,
            description=description,
            image_url=image_url,
        )

        self.validate_menu_item(new_item)
        updated_item = self.repository.update_item(new_item)
        if updated_item is None:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item_id} not found"
            )

        return updated_item