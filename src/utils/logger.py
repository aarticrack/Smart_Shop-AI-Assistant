import logging
import sys
from src.core.config import settings

def setup_logger():
    # Creating a custom logger
    logger = logging.getLogger(settings.PROJECT_NAME)
    logger.setLevel(logging.INFO)

    # Creating handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler('app_errors.log')
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.ERROR)

    # Creating formatters and adding it to handlers
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    c_format = logging.Formatter(format_str)
    f_format = logging.Formatter(format_str)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Adding handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    return logger

logger = setup_logger()