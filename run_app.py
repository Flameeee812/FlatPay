import asyncio
import logging

import uvicorn
from asgiref.wsgi import WsgiToAsgi

from server.app import app
from server.scheduler import run_scheduler
from server.utils.scheduler_utils import end_tasks
from server.logger import setup_logger_func

if __name__ == "__main__":

    setup_logger_func()
    app_logger = logging.getLogger("run_app")
    app = WsgiToAsgi(app)

    async def main():
        """
        Основная функция для запуска системы.

        1. Запускает планировщик задач.
        2. Инициализирует и запускает сервер Uvicorn с конфигурацией.
        3. Обрабатывает исключения, чтобы корректно завершить работу в случае ошибки.
        4. Закрывает планировщик задач по завершению работы приложения.
        """

        scheduler = await run_scheduler()

        try:
            app_logger.info("Приложение запущено")
            config = uvicorn.Config(app, host="127.0.0.1", port=5005, reload=True)
            server = uvicorn.Server(config)
            await server.serve()

        except Exception as e:
            app_logger.exception(f"Произошла ошибка: {e}")

        finally:
            end_tasks(scheduler=scheduler)

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        app_logger.info("Приложение завершено")
