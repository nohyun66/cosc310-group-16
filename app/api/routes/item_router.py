from fastapi import APIRouter, Depends

from app.core.security import require_admin
from app.schemas.item import Item, ItemCreate
from app.services.item_service import ItemService

router = APIRouter(prefix="/restaurants", tags=["items"])


@router.post(
    "/{restaurant_id}/menu",
    response_model=Item,
    status_code=201,
    dependencies=[Depends(require_admin)],
    responses={
        401: {"description": "A valid sign-in token is required."},
        403: {"description": "An active administrator account is required."},
        404: {"description": "Restaurant not found."},
        409: {"description": "Menu item already exists."},
    },
)
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


@router.put(
    "/{restaurant_id}/menu/{item_id}",
    response_model=Item,
    dependencies=[Depends(require_admin)],
    responses={
        401: {"description": "A valid sign-in token is required."},
        403: {"description": "An active administrator account is required."},
        404: {"description": "Restaurant or menu item not found."},
    },
)
def update_item(
    restaurant_id: str,
    item_id: str,
    updated_item: ItemCreate,
):
    return ItemService().update_menu_item(
        restaurant_id=restaurant_id,
        item_id=item_id,
        name=updated_item.name,
        cuisine=updated_item.cuisine,
        category=updated_item.category,
        price=updated_item.price,
        description=updated_item.description,
        image_url=updated_item.image_url,
    )