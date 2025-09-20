import asyncio
from pathlib import Path
from typing import AsyncIterator, List

import pandas as pd

from neochef.config import logger
from neochef.domain import Recipe

# Явно определяем имена колонок в том порядке, в котором они идут в файле
EXPECTED_COLUMNS: List[str] = [
    "id", "title", "ingredients", "directions", "link", "source", "ner"
]


def _sync_extract_chunk(reader_iterator) -> pd.DataFrame | None:
    """Synchronous helper function to be run in a separate thread."""
    try:
        return next(reader_iterator)
    except StopIteration:
        return None


class CsvExtractor:
    """
    Extracts Recipe data from a CSV file asynchronously.
    """
    def __init__(self, file_path: Path, chunksize: int = 1000):
        self.file_path = file_path
        self.chunksize = chunksize

    @logger.catch(
        message="An unexpected error occurred during async extraction.",
        onerror=lambda _: asyncio.get_running_loop().stop()
    )
    async def extract(self) -> AsyncIterator[Recipe]:
        """
        Reads the CSV file in chunks in a separate thread and yields Recipe objects.
        """
        logger.info(f"Starting async extraction from CSV file: {self.file_path}")

        try:
            with pd.read_csv(
                self.file_path,
                chunksize=self.chunksize,
                header=0, 
                names=EXPECTED_COLUMNS, 
            ) as reader:
                for chunk_df in reader:
                    for row in chunk_df.itertuples(index=False):
                        try:
                            recipe = Recipe(
                                id=str(row.id),
                                title=str(row.title),
                                ingredients=str(row.ingredients),
                                directions=str(row.directions),
                                link=str(row.link),
                                source=str(row.source),
                                ner=str(row.ner),
                            )
                            yield recipe
                        except (AttributeError, TypeError) as e:
                            logger.warning(
                                f"Skipping malformed row: {row}. Error: {e}"
                            )
            logger.success("Finished extraction.")

        except FileNotFoundError:
            logger.error(f"Extraction failed: File not found at {self.file_path}")
            raise