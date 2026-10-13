from app.schemas.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from fastapi import HTTPException

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def get_all_restaurants(self, search: str | None = None) -> list[Restaurant]:
        """Return all restaurants, or those with matching names."""
        restaurants = self.repository.get_all_restaurants()

        # Without search text, return the complete list.
        if search is None:
            return restaurants

        # Ignore capitalization and spaces around the search text.
        search_text = search.strip().lower()

        matching_restaurants = []

        for restaurant in restaurants:
            restaurant_name = restaurant.name.lower()

            # "in" checks whether the name contains the search text.
            if search_text in restaurant_name:
                matching_restaurants.append(restaurant)

        return matching_restaurants
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Restaurant:
        """Returns a restaurant by ID"""
        restaurant = self.repository.get_by_id(restaurant_id)
        if restaurant:
            return restaurant 
        raise HTTPException(status_code=404, detail=f"Restaurant ID: {restaurant_id} not found")