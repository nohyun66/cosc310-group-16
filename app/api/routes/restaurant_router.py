
from fastapi import APIRouter
from app.schemas.restaurant import Restaurant, RestaurantCreate
from app.schemas.item import Item
from app.services.restaurant_service import RestaurantService
from app.services.item_service import ItemService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[Restaurant])
def get_all_restaurants(search: str | None = None, cuisine: str | None = None):
    if search is not None or cuisine is not None:
        return RestaurantService().search_restaurants(search, cuisine)

    return RestaurantService().get_all_restaurants()


@router.get("/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    return RestaurantService().get_restaurant_by_id(restaurant_id)


@router.get("/{restaurant_id}/menu", response_model=list[Item])
def get_restaurant_menu(restaurant_id: str):
    return ItemService().get_restaurant_menu(restaurant_id)


@router.get("/{restaurant_id}/menu/{item_id}", response_model=Item)
def get_menu_item(restaurant_id: str, item_id: str):
    return ItemService().get_menu_item(restaurant_id, item_id)


@router.post("", response_model=Restaurant, status_code=201)
def create_restaurant(restaurant_data: RestaurantCreate):
    return RestaurantService().create_restaurant(restaurant_data)


@router.put("/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: str, restaurant_data: RestaurantCreate):
    return RestaurantService().update_restaurant(restaurant_id, restaurant_data)
