from pydantic import BaseModel
from models.ingredient import Ingredient


class Recipe(BaseModel):
    title: str
    servings: int
    minutes: int
    ingredients: list[Ingredient]
    source_url: str
    directions: list[str]
