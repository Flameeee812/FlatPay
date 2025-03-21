import logging
from sqlite3 import Connection

from database.db_utils.payment_utils import (
    apply_user_payment, calculate_actual_debt, archive_debt_to_last_month,
    update_debt_amount, fetch_current_debt, fetch_user_debt
)
from ..db_utils.validation_utils import is_user_exists, is_passport_numeric


service_logger = logging.getLogger("payment_services")


async def archive_debt(connection: Connection) -> bool | None:
    """
    Cервис, передающий остаток долга в столбец last_month_debt по истеченю месяца.

    Параметры:
    1. connection - подключение к базе данных
    """

    try:
        await archive_debt_to_last_month(connection)
        service_logger.info("Долг успешно перенесен в last_month_debt.")
        return None

    except Exception as e:
        service_logger.exception(f"Ошибка при архивировании долга: {e}")
        return None


async def update_debt(connection: Connection, passport: str) -> bool:
    """
    Сервис, обновляющий столбец debt после внесения показаний счетчиков.

    Параметры:
    1. connection - подключение к базе данных
    2. passport - паспортные данные пользователя
    """

    if await is_user_exists(connection, passport) is False:
        return False

    if is_passport_numeric(passport) is False:
        return False

    try:
        actual_debt = await calculate_actual_debt(connection, passport)
        await update_debt_amount(connection, actual_debt, passport)
        return True

    except Exception as e:
        service_logger.exception(f"Ошибка при обновлении долга: {e}")
        return False


async def apply_payment(connection: Connection, passport: str, new_payment) -> bool:
    """Сервис для оплаты задолжности пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
        3. new_payment - сумма оплаты задолжности
        """

    if is_passport_numeric(passport) is False:
        return False

    try:
        debt = await fetch_current_debt(connection, passport)
        new_payment = float(new_payment)
        new_debt = debt - new_payment

        await apply_user_payment(connection, new_payment, new_debt, passport)
        service_logger.info(f"Оплата для {passport} прошла успешно")
        return True

    except ValueError as VE:
        service_logger.exception(f"Введён неверный тип данных в параметр new_payment: {VE}")
        return False


async def get_debt(connection: Connection, passport: str) -> float | bool:
    """Сервис для получения информации о задолжности пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
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
