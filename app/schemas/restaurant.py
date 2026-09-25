from pydantic import BaseModel, HttpUrl
from schemas.cuisine import Cuisine

class Restaurant(BaseModel):
    id: str                     #Identifier, example: 34
    name: str                   #Display name of the restaurant, example: Hank's Grill         
    cuisine: Cuisine            #NORAM, ASIAN, MED, LATAM, EURO; here it refers to their specialty
    description: str            #Description of the restaurant
    image_url: HttpUrl          #Image URL. Placeholder: https://imgur.com/a/LCCoa9Z
    is_open: bool               #Whether the restaurant is currently open
    rating: float               #Average rating of the restaurant