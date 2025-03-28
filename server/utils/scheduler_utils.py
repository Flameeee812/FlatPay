import logging

from aiosqlite import Connection
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from server.services.db_services.payment_services import update_current_debt
from server.services.db_services.readings_services import reset_readings


scheduler_logger = logging.getLogger("scheduler_utils")


async def schedule_reset_debt(connection: Connection) -> None:
    """
    Асинхронная задача для переноса задолженности пользователей в основной долг.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await update_current_debt(connection)

    return None


async def schedule_reset_readings(connection: Connection) -> None:
    """
    Асинхронная задача для сброса показаний счётчиков пользователей.

    Параметры:
     - connection: Асинхронное соединение с базой данных.
    """

    await reset_readings(connection)

    return None


async def run_background_tasks(connection: Connection) -> AsyncIOScheduler:
    """
    Запускает фоновые задачи по обновлению долгов и сбросу показаний счётчиков.

    Каждое первое число месяца в 00:00:
     - Переносит задолженность пользователей в основной долг.
     - Обнуляет показания счётчиков.

    Параметры:
     - connection: Асинхронное соединение с базой данных.

    Возвращает:
     - AsyncIOScheduler: Планировщик фоновых задач.
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


def end_tasks(scheduler: AsyncIOScheduler) -> None:
    """
    Завершает работу планировщика задач.

    Параметры:
     - scheduler: Экземпляр AsyncIOScheduler.
    """

    scheduler.shutdown()
    scheduler_logger.info("Планировщик задач остановлен")

    return None
