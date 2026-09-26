from fastapi import APIRouter
from app.schemas.restaurant import Restaurant
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.get("", response_model=list[Restaurant])
def get_all_restaurants():
    return RestaurantService().get_all_restaurants()

@router.get("/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    return RestaurantService().get_restaurant_by_id(restaurant_id)