import asyncio
import logging

import uvicorn

from server.app import create_app
from server.config import load_config, ConfigStore
from server.scheduler import run_scheduler
from server.utils.scheduler_utils import end_tasks
from server.logger import setup_logger_func


async def main():
    """
    Основной цикл работы приложения.

    Последовательность действий:
    1. Инициализация планировщика периодических задач
    2. Создание экземпляра Quart-приложения
    3. Запуск ASGI-сервера (Uvicorn) с настройками
    4. Обработка исключений и корректное завершение работы

    Гарантирует:
    - Освобождение ресурсов планировщика при завершении
    - Логирование критических ошибок
    - Graceful shutdown при получении сигналов остановки
    """

    # Инициализация планировщика фоновых задач
    scheduler = await run_scheduler()

    # Создание ASGI-приложения
    app = create_app()

    try:
        app.logger.info("Приложение запущено")

        # Настраиваем uvicorn сервер
        server_config = uvicorn.Config(
            app,
            host="127.0.0.1",  # Локальный интерфейс
            port=5005,  # Порт по умолчанию
            reload=True)  # Автоперезагрузка в development

        app.logger.info("Старт сервера на http://127.0.0.1:5005")
        server = uvicorn.Server(server_config)
        await server.serve()

    except Exception as e:
        app.logger.exception(f"Произошла ошибка: {e}")

    finally:
        end_tasks(scheduler=scheduler)


if __name__ == "__main__":

    # Инициализация конфигурации
    config = load_config()
    ConfigStore.set_config(config)  # Глобальный доступ к конфигураци

    # Настройка системы логирования
    setup_logger_func()
    app_logger = logging.getLogger("run_app")

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        app_logger.info("Приложение завершено")
