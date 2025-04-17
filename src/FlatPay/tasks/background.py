import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from FlatPay.core import SchedulerAddTasksError
from FlatPay.tasks.jobs.reset_readings import schedule_reset_readings
from FlatPay.tasks.jobs.reset_debt import schedule_reset_debt


# Инициализируем логирование
logger = logging.getLogger("run_scheduler_tasks")


def run_scheduler_tasks(scheduler: AsyncIOScheduler, db_path: str) -> AsyncIOScheduler:
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
        # Добавляем задачу на перенос долга (каждое 1-е число месяца в 00:00)
        scheduler.add_job(
            schedule_reset_debt,     # функция, которая будет вызвана
            'cron',           # тип расписания — по времени
            day=1,                   # 1-е число каждого месяца
            hour=0,                  # в 00:00 часов
            args=[db_path]           # аргументы, передаваемые в задачу
        )

        # Добавляем задачу на сброс показаний (каждое 1-е число месяца в 00:00)
        scheduler.add_job(
            schedule_reset_readings,  # функция, которая будет вызвана
            'cron',            # тип расписания — по времени
            day=1,                    # 1-е число каждого месяца
            hour=0,                   # в 00:00 часов
            args=[db_path]            # аргументы, передаваемые в задачу
        )

        logger.info("Задачи успешно добавлены.")

    except Exception as e:
        logger.error(f"Ошибка при добавлении задач в планировщик: {e}")
        # Поднимаем исключение, чтобы вызвать обработку на более высоком уровне
        raise SchedulerAddTasksError(f"Ошибка при добавдении задач в планировщик задач")

    # Возвращаем настроенный планировщик
    return scheduler
