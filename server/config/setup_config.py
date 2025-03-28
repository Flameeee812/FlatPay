from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    """
    Класс для хранения конфигурационных данных.

    Атрибуты:
     - DATABASE_PATH (str): Путь к файлу базы данных.
     - LOG_PATH (str): Путь к файлу логирования.
    """

    DATABASE_PATH: str
    LOG_PATH: str


def load_config(path: str | None = None) -> Config:
    """
    Загружает конфигурацию из файла .env.

    Параметры:
     - path (str | None): Путь к файлу .env (по умолчанию None, ищет в корне проекта).

    Возвращает:
     - Config: Экземпляр класса с загруженными настройками.
    """

    env = Env()
    env.read_env(path)

    config = Config(
        DATABASE_PATH=env("DATABASE_PATH"),
        LOG_PATH=env("LOG_PATH")
    )

    return config
