from pydantic import BaseModel, HttpUrl, Field
from app.schemas.cuisine import Cuisine
from app.schemas.item_category import ItemCategory

class Item(BaseModel):
    id: str = Field(...,description="Unique identifier for the food item", examples=["R1-beef-pie", "R3-shawarma"])
    restaurant_id: str = Field(...,description="ID of the restaurant the item belongs to", examples=["1", "3"])
    name: str = Field(...,description="Display name of the item", examples=["Beef Pie", "Shawarma"])       
    cuisine: Cuisine = Field(...,description="The cuisine group that best fits this item")
    itemCategory: ItemCategory = Field(...,description="The food category that best fits this item")
    price: int = Field(...,description="Price in **cents**", examples=["1499"])
    description: str = Field(...,description="Description of the item")
    image_url: HttpUrl = Field(...,description="Image of the item", examples=["https://imgur.com/a/LCCoa9Z"])