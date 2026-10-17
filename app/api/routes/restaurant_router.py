from fastapi import APIRouter, Query

from app.schemas.cuisine import Cuisine
from app.schemas.restaurant import Restaurant, RestaurantCreate
from app.schemas.item import Item
from app.services.restaurant_service import RestaurantService
from app.services.item_service import ItemService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get(
    "",
    response_model=list[Restaurant],
    summary="List, search or filter restaurants",
    description=(
        "Search restaurant names without matching capitalization, "
        "filter by cuisine, or use both. No matches return an empty list."
    ),
    responses={
        422: {"description": "The cuisine value is not supported."},
    },
)
def get_all_restaurants(
    search: str | None = Query(
        default=None,
        description="Text to match within a restaurant name.",
    ),
    cuisine: Cuisine | None = Query(
        default=None,
        description="Cuisine: NORAM, ASIAN, MED, LATAM or EURO.",
    ),
):
    return RestaurantService().search_restaurants(search, cuisine)


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
    return RestaurantService().update_restaurant(
        restaurant_id,
        restaurant_data,
    )