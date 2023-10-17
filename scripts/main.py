# Imports
from pathlib import Path

from backend import TimeIt, get_logger

# Variables
logger = get_logger(Path(__file__).name)


# Functions and classes
@TimeIt
def main() -> None:
    logger.info("Started main!")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    logger.info("Completed main!")
    pass


if __name__ == "__main__":
    main()
