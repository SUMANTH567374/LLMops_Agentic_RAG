# File: logging_config.py

import logging
import sys
import yaml

# Load config.yaml for logging settings
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    log_level = config.get("logging", {}).get("level", "INFO").upper()
    log_format = config.get("logging", {}).get(
        "format",
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
except Exception:
    # Fallback defaults if config.yaml is missing or invalid
    log_level = "INFO"
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

def setup_logger(name: str = "hybrid_rag") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(stream_handler)

    return logger
