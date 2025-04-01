import logging.config

import yaml

from FlatPay.core.config import Config
from FlatPay.exceptions import LoggerSetupError


def setup_logger(config: Config) -> None:
    """
    Метод для инициализации системы логирования.

    Выполняет:
    - Создание директории для логов (если не существует)
    - Загрузку конфигурации из YAML-файла
    - Настройку корневого логгера
    """

    try:
        with open(file=config.LOG_CONFIG_PATH, mode="rt") as f:
            log_config = yaml.safe_load(f)

        logging.config.dictConfig(log_config)

    except Exception as e:
        raise LoggerSetupError(f"Ошибка при конфигурации логгирования: {e}")
