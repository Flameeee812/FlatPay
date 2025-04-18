import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uvicorn

from FlatPay.core import setup_app
from FlatPay.core import SettingsManager, Config, setup_logger
from FlatPay.tasks import run_scheduler, end_scheduler


async def main(app_config: Config):
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

    # Инициализируем Quart-приложение
    app = setup_app(app_config.SECRET_KEY)
    logger.info("Приложение запущено")

    # Инициализируем асинхронный планировщик задач
    scheduler = AsyncIOScheduler()

    try:
        # Добавляем задачи и запускаем scheduler
        run_scheduler(scheduler=scheduler, db_path=app_config.DATABASE_PATH)
        logger.info("Планировщик задач запущен")

        # Конфигурация Uvicorn-сервера (ASGI)
        server_config = uvicorn.Config(
            app=app,           # Quart-приложение как ASGI-объект
            host="127.0.0.1",  # Только локально. Поставь "0.0.0.0", чтобы открыть извне
            port=5005,         # Порт
            reload=True        # Автоперезапуск при изменениях (dev-режим)
        )

        app.logger.info("Старт сервера на http://127.0.0.1:5005")

        server = uvicorn.Server(server_config)
        await server.serve()  # Блокирующий запуск

    except Exception as e:
        app.logger.exception(f"Произошла ошибка: {e}")

    finally:
        end_scheduler(scheduler=scheduler)
        logger.info("Планировщик задач остановлен")


# Точка входа в приложение
if __name__ == "__main__":
    # Загружаем конфигурацию из .env
    SettingsManager.load_config()
    config: Config = SettingsManager.get_config()

    # Настраиваем систему логирования согласно YAML-конфигурации
    setup_logger(config=config)
    logger = logging.getLogger("main")

    try:
        # Запускаем event loop и main()
        asyncio.run(main(app_config=config))

    except KeyboardInterrupt:
        # Завершение по Ctrl+C
        logger.info("Приложение завершено")
