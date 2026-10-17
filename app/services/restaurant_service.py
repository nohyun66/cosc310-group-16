from fastapi import HTTPException

from app.schemas.cuisine import Cuisine
from app.schemas.restaurant import Restaurant, RestaurantCreate
from app.repositories.restaurant_repository import RestaurantRepository


class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def get_all_restaurants(
        self,
        cuisine: Cuisine | None = None,
    ) -> list[Restaurant]:
        """Return all restaurants, or those with the selected cuisine."""
        restaurants = self.repository.get_all_restaurants()

        if cuisine is None:
            return restaurants

        matching_restaurants = []

        for restaurant in restaurants:
            if restaurant.cuisine == cuisine:
                matching_restaurants.append(restaurant)

        return matching_restaurants

    def search_restaurants(
        self,
        search: str | None = None,
        cuisine: Cuisine | None = None,
    ) -> list[Restaurant]:
        """Apply cuisine filtering, then search the remaining names."""
        restaurants = self.get_all_restaurants(cuisine)

        if search is None:
            return restaurants

        search_text = search.strip().lower()
        matching_restaurants = []

        for restaurant in restaurants:
            if search_text in restaurant.name.lower():
                matching_restaurants.append(restaurant)

        return matching_restaurants

    def get_restaurant_by_id(self, restaurant_id: str) -> Restaurant:
        restaurant = self.repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail=f"Restaurant ID: {restaurant_id} not found",
            )

        return restaurant

    def create_restaurant(
        self,
        restaurant_data: RestaurantCreate,
    ) -> Restaurant:
        return self.repository.create_restaurant(restaurant_data)

    def update_restaurant(
        self,
        restaurant_id: str,
        restaurant_data: RestaurantCreate,
    ) -> Restaurant:
        restaurant = self.repository.update_restaurant(
            restaurant_id,
            restaurant_data,
        )

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail=f"Restaurant ID: {restaurant_id} not found",
            )

        return restaurant