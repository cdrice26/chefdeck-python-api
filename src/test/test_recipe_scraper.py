import pytest
from unittest.mock import patch, MagicMock
from services.recipe_scraper import RecipeScraper
from errors.webpage_blocked_error import WebpageBlockedError
from models.recipe import Recipe


class TestRecipeScraper:

    @pytest.fixture
    def scraper(self) -> RecipeScraper:
        return RecipeScraper("http://example.com/recipe")

    @patch("services.recipe_scraper.requests.get")
    @patch("services.recipe_scraper.scrape_html")
    @patch("services.recipe_scraper.RobotFileParserLookalike")
    def test_scrape_if_allowed_success(
        self,
        mock_robot_parser: MagicMock,
        mock_scrape_html: MagicMock,
        mock_requests_get: MagicMock,
        scraper: RecipeScraper,
    ) -> None:
        # Mocking the robot parser to allow scraping
        mock_robot_parser.return_value.can_fetch.return_value = True

        # Mocking the response from requests.get
        mock_requests_get.return_value.text = "<html></html>"

        # Mocking the scrape_html function
        mock_scraper_instance: MagicMock = MagicMock()
        mock_scraper_instance.title.return_value = "Test Recipe"
        mock_scraper_instance.total_time.return_value = 30
        mock_scraper_instance.yields.return_value = "4 servings"
        mock_scraper_instance.ingredients.return_value = ["1 cup of flour", "2 eggs"]
        mock_scraper_instance.instructions_list.return_value = [
            "Mix ingredients",
            "Bake at 350 degrees",
        ]
        mock_scrape_html.return_value = mock_scraper_instance

        # Call the method
        scraper.scrape_if_allowed()

        # Assertions
        assert scraper._title == "Test Recipe"  # type: ignore
        assert scraper._minutes == 30  # type: ignore
        assert scraper._servings == "4"  # type: ignore
        assert scraper._ingredients == ["1 cup of flour", "2 eggs"]  # type: ignore
        assert scraper._directions == ["Mix ingredients", "Bake at 350 degrees"]  # type: ignore

    @patch("services.recipe_scraper.RobotFileParserLookalike")
    def test_scrape_if_allowed_blocked(
        self, mock_robot_parser: MagicMock, scraper: RecipeScraper
    ) -> None:
        # Mocking the robot parser to block scraping
        mock_robot_parser.return_value.can_fetch.return_value = False

        # Expecting a WebpageBlockedError to be raised
        with pytest.raises(WebpageBlockedError):
            scraper.scrape_if_allowed()

    @patch("services.recipe_scraper.requests.get")
    @patch("services.recipe_scraper.scrape_html")
    @patch("services.recipe_scraper.RobotFileParserLookalike")
    def test_get_as_recipe(
        self,
        mock_robot_parser: MagicMock,
        mock_scrape_html: MagicMock,
        mock_requests_get: MagicMock,
        scraper: RecipeScraper,
    ) -> None:
        # Mocking the robot parser to allow scraping
        mock_robot_parser.return_value.can_fetch.return_value = True

        # Mocking the response from requests.get
        mock_requests_get.return_value.text = "<html></html>"

        # Mocking the scrape_html function
        mock_scraper_instance: MagicMock = MagicMock()
        mock_scraper_instance.title.return_value = "Test Recipe"
        mock_scraper_instance.total_time.return_value = 30
        mock_scraper_instance.yields.return_value = "4 servings"
        mock_scraper_instance.ingredients.return_value = ["1 cup flour", "2 eggs"]
        mock_scraper_instance.instructions_list.return_value = [
            "Mix ingredients",
            "Bake at 350 degrees",
        ]
        mock_scrape_html.return_value = mock_scraper_instance

        # Call the method to scrape
        scraper.scrape_if_allowed()

        # Get the recipe
        recipe: Recipe = scraper.get_as_recipe()

        # Assertions
        assert isinstance(recipe, Recipe)
        assert recipe.title == "Test Recipe"
        assert recipe.servings == 4
        assert recipe.minutes == 30
        assert len(recipe.ingredients) == 2
        assert recipe.ingredients[0].name == "flour"
        assert recipe.ingredients[0].unit == "cup"
        assert recipe.ingredients[0].amount == 1.0
        assert recipe.ingredients[1].name == "eggs"
        assert recipe.ingredients[1].amount == 2.0
        assert recipe.ingredients[1].unit == "count"
        assert recipe.directions == ["Mix ingredients", "Bake at 350 degrees"]
        assert recipe.source_url == "http://example.com/recipe"
