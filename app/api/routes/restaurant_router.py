from fastapi import APIRouter, Path, Query

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
        "Return stored restaurants. Optionally search by part of a name "
        "or filter by cuisine. Matching ignores capitalization. "
        "When both parameters are provided, both conditions must match. "
        "Search and filter requests with no matches return an empty list."
    ),
    responses={
        404: {
            "description": "No restaurants exist when listing without parameters."
        },
    },
)
def get_all_restaurants(
    search: str | None = Query(
        default=None,
        description="Text to match within a restaurant name.",
    ),
    cuisine: str | None = Query(
        default=None,
        description=(
            "Cuisine: NORAM, ASIAN, MED, LATAM or EURO. "
            "Matching ignores capitalization. Unsupported values return no matches."
        ),
    ),
):
    if search is not None or cuisine is not None:
        return RestaurantService().search_restaurants(search, cuisine)

    return RestaurantService().get_all_restaurants()


@router.get(
    "/{restaurant_id}",
    response_model=Restaurant,
    summary="Get restaurant details",
    description="Return the stored details of one restaurant.",
    responses={
        404: {"description": "The restaurant does not exist."},
    },
)
def get_restaurant(
    restaurant_id: str = Path(
        description="ID of the restaurant to retrieve.",
    ),
):
    return RestaurantService().get_restaurant_by_id(restaurant_id)


@router.get(
    "/{restaurant_id}/menu",
    response_model=list[Item],
    summary="Get a restaurant menu",
    description=(
        "Return menu items belonging to the selected restaurant. "
        "An existing restaurant with no items returns an empty list."
    ),
    responses={
        404: {"description": "The restaurant does not exist."},
    },
)
def get_restaurant_menu(
    restaurant_id: str = Path(
        description="ID of the restaurant whose menu is requested.",
    ),
):
    return ItemService().get_restaurant_menu(restaurant_id)


@router.get(
    "/{restaurant_id}/menu/{item_id}",
    response_model=Item,
    summary="Get menu item details",
    description="Return one menu item belonging to the selected restaurant.",
    responses={
        404: {
            "description": (
                "The restaurant or item does not exist, "
                "or the item belongs to another restaurant."
            )
        },
    },
)
def get_menu_item(
    restaurant_id: str = Path(
        description="ID of the restaurant that owns the item.",
    ),
    item_id: str = Path(
        description="ID of the menu item to retrieve.",
    ),
):
    return ItemService().get_menu_item(restaurant_id, item_id)


@router.post(
    "",
    response_model=Restaurant,
    status_code=201,
    summary="Create a restaurant",
    description=(
        "Create and save a restaurant using the supplied details. "
        "Return the saved restaurant, including its generated ID."
    ),
)
def create_restaurant(restaurant_data: RestaurantCreate):
    return RestaurantService().create_restaurant(restaurant_data)


@router.put(
    "/{restaurant_id}",
    response_model=Restaurant,
    summary="Update a restaurant",
    description=(
        "Update an existing restaurant using the supplied details. "
        "All required fields in RestaurantCreate must be provided."
    ),
    responses={
        404: {"description": "The restaurant does not exist."},
    },
)
def update_restaurant(
    restaurant_data: RestaurantCreate,
    restaurant_id: str = Path(
        description="ID of the restaurant to update.",
    ),
):
    return RestaurantService().update_restaurant(
        restaurant_id,
        restaurant_data,
    )