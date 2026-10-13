from app.schemas.restaurant import Restaurant
from app.schemas.cuisine import Cuisine
from app.repositories.restaurant_repository import RestaurantRepository
from fastapi import HTTPException

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def get_all_restaurants(
    self,
    cuisine: Cuisine | None = None,
    ) -> list[Restaurant]:
        """Return all restaurants, or those with the selected cuisine."""
        restaurants = self.repository.get_all_restaurants()

        # Without a cuisine filter, return the complete list.
        if cuisine is None:
            return restaurants

        matching_restaurants = []

        for restaurant in restaurants:
            if restaurant.cuisine == cuisine:
                matching_restaurants.append(restaurant)

        return matching_restaurants
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Restaurant:
        """Returns a restaurant by ID"""
        restaurant = self.repository.get_by_id(restaurant_id)
        if restaurant:
            return restaurant 
        raise HTTPException(status_code=404, detail=f"Restaurant ID: {restaurant_id} not found")