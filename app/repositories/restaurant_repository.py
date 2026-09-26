import json
from pathlib import Path

from app.schemas.restaurant import Restaurant

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "restaurants.json"

class RestaurantRepository:
	"""Read restaurant records from the JSON data store."""

	def get_all_restaurants(self) -> list[Restaurant] | None:
		"""
		Return all restaurants from the database as a list of Restaurant objects.
		"""
		with open(DATA_PATH, encoding="utf-8") as data_file:
			data = json.load(data_file)
			
		restaurants: list[Restaurant] = []
		for restaurant in data:
			restaurants.append(Restaurant(**restaurant))
		return restaurants
			

	def get_by_id(self, restaurant_id: str) -> Restaurant | None:
		"""
		Return a restaurant by ID, or None when it does not exist.
		"""
		for restaurant in self.get_all_restaurants():
			if restaurant.id == restaurant_id:
				return restaurant
		return None
