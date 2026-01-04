import sys
from loguru import logger

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, serialize=True, level="INFO")
    return logger