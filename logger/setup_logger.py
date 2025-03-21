import logging.config

import yaml


def setup_logger_func():
    """
    Настройка логгера с использованием конфигурации из config.yaml файла.
    """

    with open(file="logger/config.yaml", mode="rt") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)
