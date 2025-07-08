from fastapi import APIRouter, HTTPException, Query
from models.recipe import Recipe
from services.recipe_scraper import RecipeScraper, WebpageBlockedError
from urllib.parse import unquote
from typing import Annotated
from fastapi_simple_rate_limiter import rate_limiter  # type: ignore

router = APIRouter()


@router.get("/scrape-recipe")
@rate_limiter(limit=5, seconds=60)
async def scrape_recipe(url: Annotated[str, Query()]) -> Recipe:
    scraper = RecipeScraper(unquote(url))
    try:
        scraper.scrape_if_allowed()
        return scraper.get_as_recipe()
    except WebpageBlockedError:
        raise HTTPException(
            status_code=403, detail="This website does not allow scraping."
        )
