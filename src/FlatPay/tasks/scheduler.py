import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from FlatPay.tasks.background import run_scheduler_tasks
from FlatPay.core.exceptions import SchedulerStartupError


# Инициализируем логирование
logger = logging.getLogger("scheduler")


def run_scheduler(scheduler: AsyncIOScheduler, db_path: str) -> None:
    """
    Инициализирует и запускает асинхронный планировщик задач (APScheduler).

    Описание:
     - Создаёт экземпляр `AsyncIOScheduler`.
     - Запускает фоновый процесс с задачами, используя переданный путь к базе данных.
     - В случае ошибки логирует исключение и завершает выполнение.

    Параметры:
     - db_path (str): Путь к файлу базы данных.

    Исключения:
     - SchedulerStartupError: Если произошла ошибка при запуске планировщика.

    Завершает работу планировщика и корректно освобождает ресурсы после остановки.
    """

    try:
        # Регистрируем задачи в планировщике
        run_scheduler_tasks(scheduler, db_path)

        # Запускаем планировщик
        scheduler.start()
        logger.info("Планировщик запущен")

    except Exception as e:
        logger.error(f"Ошибка при запуске планировщика: {e}", exc_info=True)
        # Поднимаем исключение, чтобы вызвать обработку на более высоком уровне
        raise SchedulerStartupError("Не удалось запустить планировщик") from e


def end_scheduler(scheduler: AsyncIOScheduler):
    """
    Завершает работу планировщика APScheduler.

    Останавливает выполнение всех запланированных задач и корректно завершает работу планировщика.
    """

    # Останавливаем планировщик и все связанные задачи
    scheduler.shutdown()
    logger.info("Планировщик остановлен")
