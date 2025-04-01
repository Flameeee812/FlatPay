from dataclasses import dataclass

from environs import Env

from FlatPay.core.exceptions import ConfigLoadError, ConfigGetError


@dataclass(frozen=True)
class Config:
    """
    Неизменяемый класс для хранения конфигурационных данных.

    Атрибуты:
     - DATABASE_PATH (str): Путь к файлу базы данных.
     - LOG_CONFIG_PATH (str): Путь к файлу конфига логирования.
    """

    DATABASE_PATH: str
    LOG_CONFIG_PATH: str


class SettingsManager:
    """
    Глобальное хранилище для объекта конфигурации.
    Позволяет установить и получить конфигурацию в любом месте.
    """

    _config: Config | None = None

    @classmethod
    def load_config(cls, path: str | None = None) -> None:
        """
        Фабрика для создания переменной конфигурации.

        Параметры:
         - path (str | None): Путь к файлу .env (по умолчанию None, ищет в корне проекта).

        Возвращает:
         - Config: Экземпляр класса с загруженными настройками.
        """

        env = Env()
        env.read_env(path)  # Чтение файла .env

        try:
            config = Config(
                DATABASE_PATH=env.str("DATABASE_PATH"),
                LOG_CONFIG_PATH=env.str("LOG_CONFIG_PATH")
            )
            cls._config = config

        except Exception as e:
            raise ConfigLoadError(f"Ошибка загрузки конфигурации: {e}")

    @classmethod
    def get_config(cls) -> Config:
        """Возвращает текущий объект конфигурации."""

        if cls._config is None:
            raise ConfigGetError("Конфигурация не инициализирована! Сначала вызови load_config().")

        return cls._config
