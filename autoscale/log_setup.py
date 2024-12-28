import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(logs_folder):
    # Create a logs directory if it doesn't exist
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    # Configure logging with rotating file handler
    log_file_path = f'{logs_folder}/scale.log'
    max_log_size = 2 * 1024 * 1024  # 2 MB
    backup_count = 5  # Number of backup files to keep

    handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Set up the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
