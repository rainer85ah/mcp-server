import logging
import os
import sys


def configure_logger(name: str = "MainAgent", log_file: str = "server.log"):
    logger = logging.getLogger(name)

    if logger.handlers:  # Prevent duplicate setup
        return logger

    # Allow DEBUG in dev and INFO in prod via env var
    log_level = os.getenv("LOG_LEVEL", "DEBUG" if os.getenv("ENV") != "production" else "INFO").upper()
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel("INFO")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.debug("Logger initialized with level %s", log_level)
    return logger
