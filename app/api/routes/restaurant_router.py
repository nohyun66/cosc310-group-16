from fastapi import APIRouter, Query
from app.schemas.restaurant import Restaurant
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.get(
    "",
    response_model=list[Restaurant],
    summary="List or search restaurants",
    description="Return all restaurants, or search their names using a case-insensitive partial match.",
)
def get_all_restaurants(
    search: str | None = Query(
        default=None,
        description="Text to search for in restaurant names",
    ),
):
    return RestaurantService().get_all_restaurants(search)

@router.get("/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    return RestaurantService().get_restaurant_by_id(restaurant_id)