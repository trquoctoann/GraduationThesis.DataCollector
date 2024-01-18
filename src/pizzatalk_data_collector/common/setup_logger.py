import logging
import os

os.makedirs("logs", exist_ok=True)


def setup_logger(name, log_file_location):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file_location, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    date_format = "%Y-%m-%d %H:%M:%S"
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=date_format,
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(file_handler)
    return logger
