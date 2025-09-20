from dataclasses import dataclass


@dataclass(frozen=True)
class Ingredient:
    """
    Represents a single, normalized ingredient.
    """
    name: str  # The original name as it appears in the recipe
    normalized_name: str  # The cleaned, canonical name (e.g., "flour")