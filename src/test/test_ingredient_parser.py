# test_ingredient.py

import pytest  # type: ignore
from models.ingredient import (
    Ingredient,
)  # Adjust the import based on your file structure


class TestIngredient:
    def test_from_string_valid(self):
        # Test valid ingredient strings
        ingredient = Ingredient.from_string("1 1/2 cups sugar")
        assert ingredient.name == "sugar"
        assert ingredient.amount == 1.5
        assert ingredient.unit == "cups"

        ingredient = Ingredient.from_string("2 tablespoons olive oil")
        assert ingredient.name == "olive oil"
        assert ingredient.amount == 2.0
        assert ingredient.unit == "tablespoons"

        ingredient = Ingredient.from_string("3 to 4 ounces cheese")
        assert ingredient.name == "cheese"
        assert ingredient.amount == 3.5  # Average of 3 and 4
        assert ingredient.unit == "ounces"

    def test_from_string_with_fractions(self):
        # Test ingredient strings with fractions
        ingredient = Ingredient.from_string("½ cup flour")
        assert ingredient.name == "flour"
        assert ingredient.amount == 0.5
        assert ingredient.unit == "cup"

        ingredient = Ingredient.from_string("2 ¾ pounds apples")
        assert ingredient.name == "apples"
        assert ingredient.amount == 2.75
        assert ingredient.unit == "pounds"

    def test_from_string_empty(self):
        # Test empty string
        ingredient = Ingredient.from_string("")
        assert ingredient.name == ""
        assert ingredient.amount == 0.0
        assert ingredient.unit == "count"

    def test_from_string_with_dashes(self):
        # Test ingredient strings with dashes
        ingredient = Ingredient.from_string("1-2 cups milk")
        assert ingredient.name == "milk"
        assert ingredient.amount == 1.5  # Average of 1 and 2
        assert ingredient.unit == "cups"

    def test_from_string_with_intermediate_words(self):
        # Test ingredient strings with intermediate words
        ingredient = Ingredient.from_string("about 2 teaspoons salt")
        assert ingredient.name == "salt"
        assert ingredient.amount == 2.0
        assert ingredient.unit == "teaspoons"

        ingredient = Ingredient.from_string("to taste black pepper")
        assert ingredient.name == "black pepper"
        assert ingredient.amount == 0.0
        assert ingredient.unit == "count"  # Default unit
