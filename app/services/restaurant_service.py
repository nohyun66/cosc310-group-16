from app.schemas.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from fastapi import HTTPException

class RestaurantService:
    def __init__(self):
        self.repository = RestaurantRepository()

    def get_all_restaurants(self) -> list[Restaurant]:
        """Return all restaurants stored in the DB"""
        restaurants = self.repository.get_all_restaurants()
        if restaurants:
            return restaurants 
        raise HTTPException(status_code=404, detail="No restaurants found")
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Restaurant:
        """Returns a restaurant by ID"""
        restaurant = self.repository.get_by_id(restaurant_id)
        if restaurant:
            return restaurant 
        raise HTTPException(status_code=404, detail=f"Restaurant ID: {restaurant_id} not found")