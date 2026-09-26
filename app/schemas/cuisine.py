from enum import StrEnum

class Cuisine(StrEnum):
    """The cuisine group that fits a restaurant or item best"""
    NORAM = "NORAM"     #North American
    ASIAN = "ASIAN"     #Asian
    MED = "MED"         #Mediterranean
    LATAM = "LATAM"     #Latin American
    EURO = "EURO"       #European