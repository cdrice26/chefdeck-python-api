from pint import DimensionalityError, Quantity, UnitRegistry
from errors.invalid_ingredients_error import InvalidIngredientsError
from models.ingredient import Ingredient
from nltk.stem import WordNetLemmatizer  # type: ignore
from nltk import pos_tag  # type: ignore
import nltk  # type: ignore

nltk.data.path.append("./nltk_data")  # type: ignore

ureg = UnitRegistry()
lemmatizer = WordNetLemmatizer()


def singularize(word: str) -> str:
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"
    elif word.endswith("es") and len(word) > 2:
        return word[:-2]
    elif word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word


def lemmatize(name: str) -> str:
    pos_tagged = pos_tag(name.split())  # type: ignore
    lemmatized_name = " ".join(
        lemmatizer.lemmatize(singularize(word), pos="n" if tag.startswith("N") else "v") for word, tag in pos_tagged  # type: ignore
    )
    return lemmatized_name


class IngredientMerger:
    def __init__(self, ingredients: list[Ingredient]):
        self._ingredients = ingredients

    @property
    def ingredients(self):
        return self._ingredients

    def merge(self):
        combined_ingredients: dict[str, dict[str, Quantity]] = {}

        for ingredient in self._ingredients:
            try:
                amount = ingredient.amount
                unit = ingredient.unit
                name = ingredient.name.title()

                name = name.split(",")[0].strip()

                # Get the POS tag for the name
                lemmatized_name = lemmatize(name)

                quantity = amount * ureg(unit)

                if lemmatized_name in combined_ingredients:
                    existing_quantity = combined_ingredients[lemmatized_name][
                        "quantity"
                    ]
                    try:
                        new_quantity = existing_quantity + quantity
                        if isinstance(new_quantity, Quantity):
                            combined_ingredients[lemmatized_name][
                                "quantity"
                            ] = new_quantity
                        else:
                            raise TypeError()
                    except DimensionalityError:
                        new_entry_name = f"{lemmatized_name} ({unit})"
                        combined_ingredients[new_entry_name] = {"quantity": quantity}
                    except TypeError:
                        new_entry_name = f"{lemmatized_name} ({unit})"
                        combined_ingredients[new_entry_name] = {"quantity": quantity}
                else:
                    combined_ingredients[lemmatized_name] = {"quantity": quantity}

            except KeyError:
                raise InvalidIngredientsError()

        response: list[Ingredient] = []
        for name, data in combined_ingredients.items():
            response.append(
                Ingredient(
                    name=name,
                    amount=data["quantity"].magnitude,
                    unit=str(data["quantity"].units),
                )
            )

        self._ingredients = response
