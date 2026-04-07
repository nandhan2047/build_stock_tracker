"""
Logging configuration module.
Sets up structured logging for the application.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Configure paths
LOG_LEVEL = "INFO"
LOG_FILE = Path(__file__).parent.parent.parent / "logs" / "app.log"
LOG_FILE.parent.mkdir(exist_ok=True)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Setup and configure a logger for a module."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        log_level = level or LOG_LEVEL
        logger.setLevel(getattr(logging, log_level))

        formatter = logging.Formatter(LOG_FORMAT)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger(__name__)
