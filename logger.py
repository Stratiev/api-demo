import logging
import logging.config
import os

# global log level can be set by environment variable LOG_LEVEL
DEFAULT_LOG_LEVEL = "INFO"
log_level = os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log_level.upper()
)


def get_logger(name):
    return logging.getLogger(name)
