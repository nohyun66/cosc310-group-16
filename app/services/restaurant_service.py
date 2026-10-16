from app.schemas.restaurant import Restaurant, RestaurantCreate
from app.repositories.restaurant_repository import RestaurantRepository
from fastapi import HTTPException

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def get_all_restaurants(self) -> list[Restaurant]:
        restaurants = self.repository.get_all_restaurants()
        if restaurants:
            return restaurants 
        raise HTTPException(status_code=404, detail="No restaurants found")
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Restaurant:
        restaurant = self.repository.get_by_id(restaurant_id)
        if restaurant:
            return restaurant 
        raise HTTPException(status_code=404, detail=f"Restaurant ID: {restaurant_id} not found")
    def search_restaurants(self, search: str | None = None, cuisine: str | None = None) -> list[Restaurant]:
        restaurants = self.repository.get_all_restaurants() or []

        if search:
            restaurants = [
                restaurant for restaurant in restaurants
                if search.lower() in restaurant.name.lower()
            ]

        if cuisine:
            restaurants = [
                restaurant for restaurant in restaurants
                if restaurant.cuisine.value.lower() == cuisine.lower()
            ]

        return restaurants

    def create_restaurant(self, restaurant_data: RestaurantCreate) -> Restaurant:
        return self.repository.create_restaurant(restaurant_data)

    def update_restaurant(self, restaurant_id: str, restaurant_data: RestaurantCreate) -> Restaurant:
        restaurant = self.repository.update_restaurant(restaurant_id, restaurant_data)

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail=f"Restaurant ID: {restaurant_id} not found"
            )

        return restaurant