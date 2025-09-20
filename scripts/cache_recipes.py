import asyncio
import dataclasses
import json
from pathlib import Path

from neochef.adapters import CsvExtractor
from neochef.config import logger


async def main():
    """
    Uses the CsvExtractor to read the raw dataset and saves the extracted
    Recipe objects to a local JSONL cache file.
    """
    # Define paths
    project_root = Path(__file__).parent.parent
    input_csv_path = project_root / "data" / "RecipeNLG_dataset.csv"
    output_jsonl_path = project_root / "data" / "raw_recipes.jsonl"

    # Ensure the data directory exists
    output_jsonl_path.parent.mkdir(exist_ok=True)

    logger.info(f"Starting recipe caching process...")
    logger.info(f"Input file: {input_csv_path}")
    logger.info(f"Output cache file: {output_jsonl_path}")

    extractor = CsvExtractor(file_path=input_csv_path)
    recipe_count = 0

    try:
        with open(output_jsonl_path, "w", encoding="utf-8") as f:
            # Asynchronously iterate through recipes from the extractor
            async for recipe in extractor.extract():
                # Convert dataclass to dictionary, then to a JSON string
                recipe_dict = dataclasses.asdict(recipe)
                json_string = json.dumps(recipe_dict)
                
                # Write the JSON string as a new line in the .jsonl file
                f.write(json_string + "\n")
                
                recipe_count += 1
                if recipe_count % 1000 == 0:
                    logger.info(f"Cached {recipe_count} recipes...")

        logger.success(f"Caching complete. Total recipes cached: {recipe_count}")

    except Exception:
        logger.exception("An error occurred during the caching process.")


if __name__ == "__main__":
    asyncio.run(main())