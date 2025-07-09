from pydantic import BaseModel
from models.ingredient import Ingredient


class Recipe(BaseModel):
    """
    Representation of a Recipe.

    Properties:
        title (str): Recipe name
        servings (int): Number of servings
        minutes (int): Number of minutes the recipe takes to make
        ingredients (list[Ingredient]): List of ingredients for the recipe
        source_url (str): URL of the source website for the recipe
        directions (list[str]): List of directions in the recipe
    """

    title: str
    servings: int
    minutes: int
    ingredients: list[Ingredient]
    source_url: str
    directions: list[str]
