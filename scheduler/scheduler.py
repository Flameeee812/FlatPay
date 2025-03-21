import logging

from .scheduler_utils import run_background_tasks
from database import get_connection


scheduler_logger = logging.getLogger("scheduler")


async def run_scheduler():
    """
    Инициализирует и запускает планировщик фоновых задач.

    Подключается к базе данных и передаёт соединение в фоновый обработчик задач.
    После успешного запуска записывает событие в лог.

    Возвращаемое значение:
     - scheduler: Объект планировщика.
    """

    connection = await get_connection()

    scheduler = await run_background_tasks(connection)
    scheduler.start()
    scheduler_logger.info("Планировщик задач запущен")

    return scheduler
