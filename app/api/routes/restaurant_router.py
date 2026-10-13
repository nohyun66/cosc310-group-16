from fastapi import APIRouter, Query
from app.schemas.cuisine import Cuisine
from app.schemas.restaurant import Restaurant
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.get(
    "",
    response_model=list[Restaurant],
    summary="List or filter restaurants",
    description="Return all restaurants, or only restaurants with the selected cuisine.",
    responses={
        422: {"description": "The cuisine value is not supported."},
    },
)
def get_all_restaurants(
    cuisine: Cuisine | None = Query(
        default=None,
        description="Cuisine to filter restaurants by",
    ),
):
    return RestaurantService().get_all_restaurants(cuisine)

@router.get("/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    return RestaurantService().get_restaurant_by_id(restaurant_id)