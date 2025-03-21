import asyncio
import logging

import uvicorn
from asgiref.wsgi import WsgiToAsgi

from app import app
from scheduler import end_tasks, run_scheduler
from logger import setup_logger_func

if __name__ == "__main__":

    setup_logger_func()
    app_logger = logging.getLogger("run_app")
    app = WsgiToAsgi(app)

    async def main():
        """Функция для запуска системы"""

        scheduler = await run_scheduler()

        try:
            app_logger.info("Приложение запущено")
            config = uvicorn.Config(app, host="127.0.0.1", port=5005)
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
