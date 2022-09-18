import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = '/backend/logs'


def set_default_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # add file handler
    log_path = os.path.join(LOG_DIR, f'{logger_name}.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_handler = RotatingFileHandler(log_path, mode='a', maxBytes=100000000, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
