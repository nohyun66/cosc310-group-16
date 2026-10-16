
import json
from pathlib import Path

from app.schemas.restaurant import Restaurant, RestaurantCreate

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "restaurants.json"


class RestaurantRepository:

    def get_all_restaurants(self) -> list[Restaurant]:
        with open(DATA_PATH, encoding="utf-8") as data_file:
            data = json.load(data_file)

        restaurants = []
        for restaurant in data:
            restaurants.append(Restaurant(**restaurant))

        return restaurants

    def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        for restaurant in self.get_all_restaurants():
            if restaurant.id == restaurant_id:
                return restaurant
        return None

    def create_restaurant(self, restaurant_data: RestaurantCreate) -> Restaurant:
        restaurants = self.get_all_restaurants()

        new_id = str(max((int(r.id) for r in restaurants), default=0) + 1)

        new_restaurant = Restaurant(
            id=new_id,
            **restaurant_data.model_dump()
        )

        restaurants.append(new_restaurant)

        with open(DATA_PATH, "w", encoding="utf-8") as data_file:
            json.dump(
                [r.model_dump(mode="json") for r in restaurants],
                data_file,
                indent=2
            )

        return new_restaurant

    def update_restaurant(self, restaurant_id: str, restaurant_data: RestaurantCreate) -> Restaurant | None:
        restaurants = self.get_all_restaurants()

        for index, restaurant in enumerate(restaurants):
            if restaurant.id == restaurant_id:
                updated_restaurant = Restaurant(
                    id=restaurant_id,
                    **restaurant_data.model_dump()
                )

                restaurants[index] = updated_restaurant

                with open(DATA_PATH, "w", encoding="utf-8") as data_file:
                    json.dump(
                        [r.model_dump(mode="json") for r in restaurants],
                        data_file,
                        indent=2
                    )

                return updated_restaurant

        return None
