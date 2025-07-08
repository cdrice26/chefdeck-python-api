from recipe_scrapers import scrape_html
from robotexclusionrulesparser import RobotFileParserLookalike  # type: ignore
import requests
from errors.webpage_blocked_error import WebpageBlockedError
from models.ingredient import Ingredient
from models.recipe import Recipe


class RecipeScraper:
    _url: str
    _can_scrape: bool
    _title: str
    _minutes: int
    _servings: int
    _ingredients: list[str]
    _directions: list[str]

    def __init__(self, url: str) -> None:
        self._url = url
        self._can_scrape = False

    def is_allowed(self):
        robot_parser = RobotFileParserLookalike()
        self._can_scrape = robot_parser.can_fetch("cookybot", self._url)  # type: ignore

    def scrape_if_allowed(self):
        self.is_allowed()
        if not self._can_scrape:
            raise WebpageBlockedError()
        html: str = requests.get(self._url, headers={"User-Agent": "cookybot"}).text
        scraper = scrape_html(html, org_url=self._url)
        self._title = scraper.title()
        self._minutes = scraper.total_time()
        servings = scraper.yields()  # type: ignore
        self._servings = servings.split(" ")[0]  # type: ignore
        self._ingredients = scraper.ingredients()
        self._directions = scraper.instructions_list()

    def get_as_recipe(self):
        return Recipe(
            title=self._title,
            servings=int(self._servings),
            minutes=int(self._minutes),
            ingredients=[Ingredient.from_string(ing) for ing in self._ingredients],
            directions=self._directions,
            source_url=self._url,
        )
