import logging
from asyncio import create_task, gather
from sqlite3 import Connection

from database.db_utils.payment_utils import (
    apply_user_payment, calculate_base_debt, update_current_month_debt,
    update_next_month_debt, fetch_user_debt, reset_next_month_debt
)
from ..db_utils.validation_utils import is_user_exists, is_passport_numeric


service_logger = logging.getLogger("payment_services")


async def update_current_debt(connection: Connection) -> None:
    """
    Cервис, передающий значение долга из столбаца next_month_debt в debt.

    После выполнения операции столбец next_month_debt обнуляется.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    try:
        task1 = create_task(update_current_month_debt(connection))
        task2 = create_task(reset_next_month_debt(connection))

        await gather(task1, task2)
        service_logger.info("Долг успешно перенесен в debt.")
        return None

    except Exception as e:
        service_logger.exception(f"Ошибка при попытке перенести долг: {e}")
        return None


async def update_next_debt(connection: Connection, passport: str, readings: dict[str, str]) -> bool:
    """
    Сервис, обновляющий столбец next_month_debt после внесения показаний счетчиков.

    Если пользователь существует, рассчитывается новый долг на основании тарифов,
    после чего обновляется соответствующий столбец в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - bool: True, если столбец next_month_debt обновился, иначе False.
    """

    if await is_user_exists(connection, passport) is False:
        return False

    if is_passport_numeric(passport) is False:
        return False

    try:
        debt = calculate_base_debt(readings)
        await update_next_month_debt(connection, debt, passport)
        service_logger.info(f"next_month_debt для {passport} успешно обновлён.")
        return True

    except Exception as e:
        service_logger.exception(f"Ошибка при обновлении next_month_debt: {e}")
        return False


async def apply_payment(connection: Connection, passport: str, new_payment: str) -> bool:
    """
    Сервис для оплаты задолжности пользователя.

    Проверяет корректность данных, рассчитывает новый долг
    и обновляет его в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.
     - new_payment (str): сумма оплаты задолжности.

    Возвращаемое значение:
     -bool: False, если оплата не прошла.
     """

    if is_passport_numeric(passport) is False:
        return False

    try:
        debt = await fetch_user_debt(connection, passport)
        new_payment = float(new_payment)
        new_debt = debt - new_payment

        await apply_user_payment(connection, new_payment, new_debt, passport)
        service_logger.info(f"Оплата для {passport} прошла успешно")
        return True

    except ValueError as VE:
        service_logger.exception(f"Введён неверный тип данных в параметр new_payment: {VE}")
        return False


async def get_debt(connection: Connection, passport: str) -> float | bool:
    """
    Сервис для получения информации о задолжности пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - float: Текущий долг пользователя.
     - bool: False, если долг отсутствует.
    """

    if is_passport_numeric(passport) is False:
        return False

    if await is_user_exists(connection, passport) is False:
        return False

    try:
        debt = await fetch_user_debt(connection, passport)
        return debt

    except Exception as e:
        service_logger.exception(f"Ошибка при попытке отобразить данные о задолжности: {e}")
        return False
