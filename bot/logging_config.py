import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Configures beautiful logging to both console and a rotating log file.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    # File Handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "trading_bot.log"), 
        maxBytes=1024 * 1024, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Root Logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
