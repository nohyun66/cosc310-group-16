from pydantic import BaseModel, HttpUrl, Field
from app.schemas.cuisine import Cuisine

class Restaurant(BaseModel):
    id: str = Field(..., description="Unique Identifier for the restaurant", examples=["34", "12"])
    name: str = Field(..., description="Display name of the restaurant", examples=["Hank's Grill"])       
    cuisine: Cuisine = Field(..., description="The cuisine specialty of the restaurant")
    description: str = Field(..., description="Description of the restaurant")
    image_url: HttpUrl = Field(...,description="URL for the image of the restaurant", examples=["https://imgur.com/a/LCCoa9Z"])
    is_open: bool = Field(...,description="Whether the restaurant is currently open")
    rating: float = Field(...,description="Average rating of the restaurant")