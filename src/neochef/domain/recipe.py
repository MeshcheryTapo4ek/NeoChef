from dataclasses import dataclass


@dataclass(frozen=True)
class Recipe:
    """
    Represents a recipe as extracted from the raw data source.
    The fields directly correspond to the structure of the RecipeNLG JSON data.
    """
    id: str
    title: str
    ingredients: str  # Raw ingredient string, to be parsed later
    directions: str
    link: str
    source: str
    ner: str  # Named Entity Recognition string of ingredients