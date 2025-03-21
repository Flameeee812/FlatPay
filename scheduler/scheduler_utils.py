import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.db_services.payment_services import archive_debt
from database.db_services.readings_services import reset_readings


scheduler_logger = logging.getLogger("scheduler_utils")


async def schedule_reset_debt(connection):
    await archive_debt(connection)


async def schedule_reset_readings(connection):
    await reset_readings(connection)


async def run_background_tasks(connection):
    """
    Функция для старта фоновых задач по обновлению долгов и сбросу показаний счётчиков.

    Параметры:
    1. connection - подключение к базе данных
"""

    scheduler = AsyncIOScheduler()

    try:
        scheduler.add_job(schedule_reset_debt, 'cron', day=1, hour=00, args=[connection])
        scheduler_logger.info("Задача reset_to_zero_debt успешно добавлена.")
    except Exception as e:
        scheduler_logger.error(f"Ошибка при добавлении задачи reset_to_zero_debt: {e}")

    try:
        scheduler.add_job(schedule_reset_readings, 'cron', day=1, hour=00, args=[connection])
        scheduler_logger.info("Задача reset_to_zero_readings успешно добавлена.")
    except Exception as e:
        scheduler_logger.error(f"Ошибка при добавлении задачи reset_to_zero_readings: {e}")

    return scheduler


def end_tasks(scheduler) -> None:
    """Функция для завершения работы планировщика"""

    scheduler.shutdown()
    scheduler_logger.info("Планировщик задач остановлен")

    return None
