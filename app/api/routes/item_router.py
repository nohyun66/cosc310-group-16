from fastapi import APIRouter
from app.schemas.item import Item, ItemCreate
from app.services.item_service import ItemService

router = APIRouter(prefix="/restaurants", tags=["items"])


@router.post("/{restaurant_id}/menu", response_model=Item, status_code=201)
def create_item(restaurant_id: str, new_item: ItemCreate):
    return ItemService().create_menu_item(
        restaurant_id=restaurant_id,
        name=new_item.name,
        cuisine=new_item.cuisine,
        category=new_item.category,
        price=new_item.price,
        description=new_item.description,
        image_url=new_item.image_url,
    )