import pytest
from models.ingredient import Ingredient
from services.ingredient_merger import (
    singularize,
    lemmatize,
    IngredientMerger,
)


# Test cases for singularize function
def test_singularize():
    assert singularize("cats") == "cat"
    assert singularize("dogs") == "dog"
    assert singularize("bunnies") == "bunny"
    assert singularize("foxes") == "fox"
    assert singularize("child") == "child"  # No change
    assert singularize("potato") == "potato"  # No change
    assert singularize("berries") == "berry"


# Test cases for lemmatize function
def test_lemmatize():
    assert lemmatize("running") == "run"
    assert lemmatize("cats and dogs") == "cat and dog"
    assert lemmatize("went") == "go"
    assert lemmatize("children") == "child"


# Test cases for IngredientMerger class
def test_ingredient_merger():
    # Create some mock ingredients
    ingredient1 = Ingredient(name="Tomato", amount=2, unit="kg")
    ingredient2 = Ingredient(name="Tomatoes", amount=1, unit="kg")
    ingredient3 = Ingredient(name="Onion", amount=0.5, unit="kg")
    ingredient4 = Ingredient(name="Onions", amount=1, unit="g")

    ingredients = [ingredient1, ingredient2, ingredient3, ingredient4]
    merger = IngredientMerger(ingredients)

    # Perform the merge
    merger.merge()

    # Check the merged ingredients
    merged_ingredients = merger.ingredients

    # Check if the tomatoes are merged correctly
    assert len(merged_ingredients) == 2  # Should be 2 unique ingredients after merging
    assert merged_ingredients[0].name == "Tomato"  # Check for the first ingredient
    assert merged_ingredients[0].amount == 3  # 2 kg + 1 kg = 3 kg
    assert merged_ingredients[1].name == "Onion"  # Check for the second ingredient
    assert (
        merged_ingredients[1].amount == 0.501
    )  # 0.5 kg + 1 g = 0.501 kg (should be converted correctly)


# Run the tests
if __name__ == "__main__":
    pytest.main()
