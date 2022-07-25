import logging


def set_default_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # add file handler
    file_handler = logging.FileHandler('../log/main_logger.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
