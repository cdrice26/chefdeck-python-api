from recipe_scrapers import scrape_html
from robotexclusionrulesparser import RobotFileParserLookalike  # type: ignore
import requests
from errors.webpage_blocked_error import WebpageBlockedError
from models.ingredient import Ingredient
from models.recipe import Recipe
import os


class RecipeScraper:
    """
    Utility class for scraping recipes with the recipe-scrapers library.

    Parameters:
        url (str): The url to scrape
    """

    _url: str
    _can_scrape: bool
    _title: str
    _minutes: int
    _servings: int
    _ingredients: list[str]
    _directions: list[str]
    _user_agent: str

    def __init__(self, url: str) -> None:
        self._url = url
        self._can_scrape = False
        ua_env_var = os.getenv("USER_AGENT")
        self._user_agent = "chefdeckdemo" if ua_env_var is None else ua_env_var

    def is_allowed(self) -> bool:
        """
        Sets the can_scrape private property based on whether the provided url can be scraped and returns it.

        Returns:
            bool: Whether or not the provided URL can be scraped.
        """
        robot_parser = RobotFileParserLookalike()
        self._can_scrape = robot_parser.can_fetch(self._user_agent, self._url)  # type: ignore
        return self._can_scrape  # type: ignore

    def scrape_if_allowed(self):
        """
        Scrapes the recipe if the website's robots.txt allows scraping the page.
        Data is stored internally and can be fetched with get_as_recipe().
        """
        self.is_allowed()
        if not self._can_scrape:
            raise WebpageBlockedError()
        html: str = requests.get(
            self._url, headers={"User-Agent": self._user_agent}
        ).text
        scraper = scrape_html(html, org_url=self._url)
        self._title = scraper.title()
        self._minutes = scraper.total_time()
        servings = scraper.yields()  # type: ignore
        self._servings = servings.split(" ")[0]  # type: ignore
        self._ingredients = scraper.ingredients()
        self._directions = scraper.instructions_list()

    def get_as_recipe(self):
        """
        Returns the scraped recipe (if it exists) as a Recipe model instance.

        Returns:
            Recipe: The scraped recipe
        """
        return Recipe(
            title=self._title,
            servings=int(self._servings),
            minutes=int(self._minutes),
            ingredients=[Ingredient.from_string(ing) for ing in self._ingredients],
            directions=self._directions,
            source_url=self._url,
        )
