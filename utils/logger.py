import logging
import os

LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO")

def setup_logger(name="weather_app"):
    """Set up a logger with the specified name and log level."""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)
    fh = logging.FileHandler(f"app.log")
    fh.setLevel(LOG_LEVEL)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger