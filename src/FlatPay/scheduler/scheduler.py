import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from FlatPay.utils.schedulers import run_background_tasks
from FlatPay.core.exceptions import SchedulerStartupError


scheduler_logger = logging.getLogger("scheduler")


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
        run_background_tasks(scheduler, db_path)
        scheduler.start()
        scheduler_logger.info("Планировщик запущен")

    except Exception as e:
        scheduler_logger.error(f"Ошибка при запуске планировщика: {e}", exc_info=True)
        raise SchedulerStartupError("Не удалось запустить планировщик") from e


def end_scheduler(scheduler: AsyncIOScheduler):
    """
    Завершает работу планировщика APScheduler.

    Останавливает выполнение всех запланированных задач и корректно завершает работу планировщика.
    """

    scheduler.shutdown()
    scheduler_logger.info("Планировщик остановлен")
