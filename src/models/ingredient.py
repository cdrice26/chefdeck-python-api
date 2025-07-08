from fractions import Fraction
import re

from pydantic import BaseModel

terms = [
    "cup",
    "cups",
    "tablespoon",
    "tablespoons",
    "teaspoon",
    "teaspoons",
    "pint",
    "pints",
    "quart",
    "quarts",
    "gallon",
    "gallons",
    "oz",
    "ounces",
    "ounce",
    "pound",
    "pounds",
    "lb",
    "lbs",
    "tsp",
    "tbsp",
    "tbs",
    "tbsps",
    "gal",
    "gals",
]

intermediate_words = ["to", "about"]


def replace_fractions(text: str) -> str:
    """
    Replaces common fraction symbols with the equivalent string representation.

    Parameters:
        text (str): The string to be processed.

    Returns:
        str: The modified string with fraction symbols replaced.
    """
    replacements = {
        "½": "1/2",
        "¼": "1/4",
        "¾": "3/4",
        "⅓": "1/3",
        "⅔": "2/3",
        "⅕": "1/5",
        "⅖": "2/5",
        "⅗": "3/5",
        "⅘": "4/5",
        "⅙": "1/6",
        "⅚": "5/6",
        "⅐": "1/7",
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return text


class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str

    @classmethod
    def from_string(cls, text: str) -> "Ingredient":
        parser = cls._Parser(text)
        return cls(name=parser.name, amount=parser.amount, unit=parser.unit)

    class _Parser:
        def __init__(self, text: str):
            self.name = ""
            self.amount = 0.0
            self.unit = "count"
            self._split_ingredient_str(text)

        def _split_ingredient_str(self, text: str):
            words = text.split(" ")
            count_field = ""
            current_word = words[0]
            while (
                current_word in intermediate_words
                or current_word in terms
                or current_word.isdigit()
                or re.match(r"^\d*\.?\d*[/]\d*\.?\d*$", current_word)
                or re.match(r"^\d*\.\d*$", current_word)
            ):
                count_field += current_word + " "
                words.pop(0)
                current_word = words[0]
            count_field = count_field.strip()
            self.name = " ".join(words).strip()
            self._parse_measurement(count_field)

        def _parse_measurement(self, s: str):
            s = replace_fractions(s)
            s = s.replace("-", " to ")  # normalize dashes

            # Tokenize and parse mixed numbers like "1 1/2"
            tokens = s.split()
            values: list[str] = []
            i = 0

            while i < len(tokens):
                part = tokens[i]
                if part in {"to", "and"}:
                    values.append(part)
                    i += 1
                elif i + 1 < len(tokens):
                    # Try parsing as mixed number: "1 1/2"
                    try:
                        val = float(Fraction(tokens[i])) + float(
                            Fraction(tokens[i + 1])
                        )
                        values.append(str(val))
                        i += 2
                    except (ValueError, ZeroDivisionError):
                        values.append(part)
                        i += 1
                else:
                    values.append(part)
                    i += 1

            # Check for range
            if "to" in values:
                try:
                    idx = values.index("to")
                    val1 = float(values[idx - 1])
                    val2 = float(values[idx + 1])
                    self.amount = (val1 + val2) / 2
                    unit_tokens = values[idx + 2 :]
                except (IndexError, ValueError):
                    self.amount = 0.0
                    unit_tokens = []
            else:
                # Sum all valid numerical values before first alpha token
                self.amount = 0.0
                unit_tokens: list[str] = []
                for token in values:
                    if re.fullmatch(r"[a-zA-Z]+", token):
                        unit_tokens.append(token)
                    else:
                        try:
                            self.amount += float(Fraction(token))
                        except (ValueError, ZeroDivisionError):
                            pass

            # Find first valid unit token
            for word in unit_tokens + values:
                if re.fullmatch(r"[a-zA-Z]+", word):
                    self.unit = word
                    break
