from pydantic import BaseModel, HttpUrl
from schemas.cuisine import Cuisine
from app.schemas.item_category import ItemCategory

class Item(BaseModel):
    id: str                     #Identifier, example: R1-beef-pie
    restaurant_id: int          #ID of the restaurant the item belongs to, example: 1
    name: str                   #Display name of the item, example: Beef Pie          
    cuisine: Cuisine            #NORAM, ASIAN, MED, LATAM, EURO
    itemCategory: ItemCategory  #Side, Main, Dessert, Drink, Soup
    price: int                  #Price in **cents**, example: 1499 = $14.99
    description: str            #Description of the item
    image_url: HttpUrl          #Image URL. Placeholder: https://imgur.com/a/LCCoa9Z