import logging.config
import os

import yaml

from ..config import ConfigStore


def create_log_dir() -> None:
    """
     Функция для создания директории с лог-файлами.
    """

    config = ConfigStore.get_config()
    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)

    return None


def setup_logger_func() -> None:
    """
    Настройка логгера с использованием конфигурации из config.yaml файла.
    """

    # Создаем директорию для логов
    create_log_dir()

    # Загружаем конфигурацию
    with open(file="server/logger/config.yaml", mode="rt") as f:
        log_config: dict = yaml.safe_load(f)
    logging.config.dictConfig(log_config)

    return None
