from enum import StrEnum

class ItemCategory(StrEnum):
    """The food category that fits an item best"""
    SIDE = "Side"
    MAIN = "Main"
    DESSERT = "Dessert"
    DRINK = "Drink"
    SOUP = "Soup"