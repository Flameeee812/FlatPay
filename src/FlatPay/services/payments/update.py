import logging
from asyncio import create_task, gather

from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.database.repositories.payments_repo import (
    update_current_month_debt_repo, update_next_month_debt_repo, reset_next_month_debt_repo
)
from FlatPay.utils.calculate_base_debt import calculate_base_debt
from FlatPay.app.models import Readings


# Инициализируем логирование
logger = logging.getLogger("payments_services")


async def update_current_debt(connection: Connection) -> None:
    """
    Сервис для переноса задолженности на текущий расчётный месяц.

    Переносит значение из столбца next_month_debt в столбец debt,
    после чего обнуляет next_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    try:
        # Создаем задачу, складывающую current_month_debt и next_month_debt
        task1 = create_task(update_current_month_debt_repo(connection))
        # Создаем задачу,обнуляющую next_month_debt
        task2 = create_task(reset_next_month_debt_repo(connection))

        await gather(task1, task2)
        logger.info("Долг успешно перенесён в debt.")

    except Exception as e:
        logger.exception(f"Ошибка при попытке перенести долг: {e}")


async def update_next_debt(connection: Connection, email: EmailStr, readings: Readings) -> bool:
    """
    Сервис для расчёта и сохранения долга на следующий месяц.

    Вычисляет задолженность на основе новых показаний счётчиков
    и сохраняет её в столбец next_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.
     - readings (Readings): Показания счётчиков.

    Возвращаемое значение:
     - bool: True, если значение успешно обновлено, иначе False.
    """

    try:
        # Высчитываем долг по казанскому тарифу
        debt: float = calculate_base_debt(readings)

        # Передаем значение debt в столбец next_month_debt
        await update_next_month_debt_repo(connection, debt, email)
        logger.info(f"next_month_debt для {email} успешно обновлён.")
        return True

    except Exception as e:
        logger.exception(f"Ошибка при обновлении next_month_debt: {e}")
        return False
