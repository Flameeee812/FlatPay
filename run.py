import asyncio
import logging

import uvicorn

from FlatPay.app import setup_app
from FlatPay.core import SettingsManager, setup_logger
from FlatPay.scheduler import run_scheduler


async def main(db_path):
    """
    Основной цикл работы приложения.

    Последовательность действий:
    1. Инициализация планировщика периодических задач
    2. Создание экземпляра Quart-приложения
    3. Запуск ASGI-сервера (Uvicorn) с настройками
    4. Обработка исключений и корректное завершение работы

    Гарантирует:
    - Корректное завершение работы планировщика при остановке приложения.
    - Логирование критических ошибок.
    - Плавное завершение работы при получении сигнала остановки.
    """

    # Создание ASGI-приложения
    app = setup_app()

    # Запуск планировщика задач
    await run_scheduler(db_path=db_path)

    try:
        app_logger.info("Приложение запущено")

        # Настраиваем uvicorn сервер
        server_config = uvicorn.Config(
            app,  # Приложение
            host="127.0.0.1",  # Локальный интерфейс
            port=5005,  # Порт по умолчанию
            reload=True)  # Автоперезагрузка в development

        app.logger.info("Старт сервера на http://127.0.0.1:5005")
        server = uvicorn.Server(server_config)
        await server.serve()

    except Exception as e:
        app.logger.exception(f"Произошла ошибка: {e}")


if __name__ == "__main__":

    # Инициализация конфигурации
    SettingsManager.load_config()
    config = SettingsManager.get_config()

    # Настройка системы логирования
    setup_logger(config=config)
    app_logger = logging.getLogger("main")

    try:
        asyncio.run(main(config.DATABASE_PATH))

    except KeyboardInterrupt:
        app_logger.info("Приложение завершено")
