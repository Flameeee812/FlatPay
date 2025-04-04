import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from FlatPay.database import get_connection, close_connection
from FlatPay.services.payments import update_current_debt
from FlatPay.services.readings import reset_readings
from FlatPay.core.exceptions import SchedulerAddTasksError


scheduler_logger = logging.getLogger("schedulers")


async def schedule_reset_debt(db_path: str) -> None:
    """
    Переносит задолженность пользователей в основной долг.

    Описание:
    - Устанавливает соединение с базой данных.
    - Обновляет текущий долг пользователей.

    Параметры:
    - db_path (str): Путь к файлу базы данных.
    """

    try:
        connection = await get_connection(path=db_path)
        await update_current_debt(connection)
        await close_connection(connection)

    except Exception as e:
        scheduler_logger.warning(f"Ошибка при выполнении задачи schedule_reset_debt: {e}")


async def schedule_reset_readings(db_path: str) -> None:
    """
    Обнуляет показания счётчиков пользователей.

    Описание:
    - Устанавливает соединение с базой данных.
    - Сбрасывает данные о показаниях счётчиков.

    Параметры:
    - db_path (str): Путь к файлу базы данных.
    """

    try:
        connection = await get_connection(path=db_path)
        await reset_readings(connection)
        await close_connection(connection)

    except Exception as e:
        scheduler_logger.warning(f"Ошибка при выполнении задачи schedule_reset_readings: {e}")


def run_background_tasks(scheduler: AsyncIOScheduler, db_path: str) -> AsyncIOScheduler:
    """
    Запускает фоновые задачи в планировщике APScheduler.

    Описание:
     - Каждый месяц, 1-го числа в 00:00:
       - Переносит задолженность пользователей в основной долг.
       - Обнуляет показания счётчиков.

    Параметры:
     - scheduler (AsyncIOScheduler): Экземпляр планировщика.
     - db_path (str): Путь к файлу базы данных.

    Исключения:
     - SchedulerAddTasksError: Ошибка при добавлении задач.

    Возвращает:
     - scheduler (AsyncIOScheduler): Настроенный планировщик задач.
    """

    try:
        # Добавляем первую задачу
        scheduler.add_job(schedule_reset_debt, 'cron', day=1, hour=00, args=[db_path])
        # Добавляем вторую задачу
        scheduler.add_job(schedule_reset_readings, 'cron', day=1, hour=00, args=[db_path])

        scheduler_logger.info("Задачи успешно добавлены.")

    except Exception as e:
        scheduler_logger.error(f"Ошибка при добавдении задач в планировщик задач: {e}")
        raise SchedulerAddTasksError(f"Ошибка при добавдении задач в планировщик задач")

    return scheduler
