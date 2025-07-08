from fastapi import APIRouter, HTTPException
from fastapi_simple_rate_limiter import rate_limiter  # type: ignore
from errors.invalid_ingredients_error import InvalidIngredientsError
from models.ingredient import Ingredient
from services.ingredient_merger import IngredientMerger

router = APIRouter()


@router.post("/merge-ingredients")
@rate_limiter(limit=20, seconds=60)
async def merge_ingredients(ingredients: list[Ingredient]) -> list[Ingredient]:
    try:
        merger = IngredientMerger(ingredients)
        merger.merge()
        return merger.ingredients
    except InvalidIngredientsError:
        raise HTTPException(
            status_code=400,
            detail="Each ingredient must have 'amount', 'unit', and 'name'",
        )
