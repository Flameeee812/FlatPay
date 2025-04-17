import logging.config

import yaml

from FlatPay.core.config import Config
from FlatPay.core.exceptions import LoggerSetupError


def setup_logger(config: Config) -> None:
    """
    Метод для инициализации системы логирования.

    Выполняет:
    - Создание директории для логов (если не существует)
    - Загрузку конфигурации из YAML-файла
    - Настройку корневого логгера
    """

    try:
        # Открываем YAML-файл с конфигурацией логирования по указанному пути
        with open(file=config.LOG_CONFIG_PATH, mode="rt") as f:
            log_config = yaml.safe_load(f)

        # Применяем конфигурацию логгирования (устанавливаем уровни, хендлеры, форматтеры и т.д.)
        logging.config.dictConfig(log_config)

    except Exception as e:
        # При любой ошибке — выбрасываем собственное исключение
        raise LoggerSetupError(f"Ошибка при конфигурации логгирования: {e}")
