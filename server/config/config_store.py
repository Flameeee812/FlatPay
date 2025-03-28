from .load_config import Config


class ConfigStore:
    """
    Глобальное хранилище для объекта конфигурации.
    Позволяет установить и получить конфигурацию в любом месте.
    """

    _config: Config | None = None

    @classmethod
    def set_config(cls, config) -> None:
        """Сохраняет объект конфигурации."""

        cls._config = config

    @classmethod
    def get_config(cls) -> Config:
        """Возвращает текущий объект конфигурации."""

        if cls._config is None:
            raise RuntimeError("Конфигурация не инициализирована! Сначала вызови set_config().")

        return cls._config
