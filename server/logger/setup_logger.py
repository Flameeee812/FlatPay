import logging.config
import os

import yaml

from ..config import config


def create_log_dir():
    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)


def setup_logger_func() -> None:
    """
    Настройка логгера с использованием конфигурации из config.yaml файла.
    """

    create_log_dir()

    with open(file="server/logger/config.yaml", mode="rt") as f:
        log_config = yaml.safe_load(f)
    logging.config.dictConfig(log_config)

    return None
