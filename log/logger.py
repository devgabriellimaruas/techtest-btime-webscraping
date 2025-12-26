import os
import logging
from datetime import datetime

from src.config import DATA_DIR


# Log filename with timestamp
log_filename = os.path.join(DATA_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

def get_logger(name=None):
    return logging.getLogger(name)
