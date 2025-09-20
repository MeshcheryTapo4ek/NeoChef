import sys

from loguru import logger

# 1. Remove the default, pre-configured handler.
logger.remove()

# 2. Add a new handler to send logs to the console (stderr).
logger.add(
    sink=sys.stderr,
    level="INFO",  # Log messages of severity INFO and higher.
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    colorize=True,
)
