import logging

from .scheduler_utils import run_background_tasks
from database import get_connection


scheduler_logger = logging.getLogger("scheduler")


async def run_scheduler():
    connection = await get_connection()

    scheduler = await run_background_tasks(connection)
    scheduler.start()
    scheduler_logger.info("Планировщик задач запущен")

    return scheduler
