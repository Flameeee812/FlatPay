import logging
from asyncio import create_task, gather
from sqlite3 import Connection

from FlatPay.database.repositories.payments import (
    apply_user_payment, update_current_month_debt,
    update_next_month_debt, fetch_user_debt, reset_next_month_debt
)
from FlatPay.utils.debt_calculator import calculate_base_debt
from FlatPay.utils.formatters import normalize_passport
from FlatPay.utils.validators import validate_passport
from FlatPay.app.models import Readings, NewPayment
from FlatPay.core.exceptions import PassportIsNotNumericError, PassportNotFoundError, PassportIsInvalidError


service_logger = logging.getLogger("payments")


async def update_current_debt(connection: Connection) -> None:
    """
    Сервис, передающий значение долга из столбца next_month_debt в debt.

    После выполнения операции столбец next_month_debt обнуляется.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.

    Возвращаемое значение:
     - None
    """

    try:
        task1 = create_task(update_current_month_debt(connection))
        task2 = create_task(reset_next_month_debt(connection))

        await gather(task1, task2)
        service_logger.info("Долг успешно перенесён в debt.")

    except Exception as e:
        service_logger.exception(f"Ошибка при попытке перенести долг: {e}")


async def update_next_debt(connection: Connection, passport: str, readings: Readings) -> bool:
    """
    Сервис для обновления столбца next_month_debt после внесения показаний счётчиков.

    Для указанного пользователя рассчитывается новый долг на основании потребления ресурсов
    (исходя из переданных показаний счётчиков), после чего обновляется значение в столбце
    next_month_debt в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.
     - readings (Readings): Показания счётчиков для расчёта долга.

    Возвращаемое значение:
     - bool: True, если столбец next_month_debt успешно обновлён, иначе False.
    """

    try:
        await validate_passport(connection, passport)
    except (PassportIsNotNumericError, PassportIsInvalidError, PassportNotFoundError) as e:
        service_logger.warning(e)
        return False

    try:
        passport = normalize_passport(passport)
        debt = calculate_base_debt(readings)
        await update_next_month_debt(connection, debt, passport)
        service_logger.info(f"next_month_debt для {passport} успешно обновлён.")
        return True

    except Exception as e:
        service_logger.exception(f"Ошибка при обновлении next_month_debt: {e}")
        return False


async def apply_payment(connection: Connection, passport: str, new_payment: NewPayment) -> bool:
    """
    Сервис для применения платежа и обновления задолженности пользователя.

    Проверяет корректность данных о пользователе, рассчитывает новый долг
    на основе внесённой оплаты и обновляет его в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.
     - new_payment (NewPayment): Сумма оплаты задолженности.

    Возвращаемое значение:
     - bool: True, если оплата прошла успешно и долг был обновлён, иначе False.
    """

    try:
        await validate_passport(connection, passport)
    except (PassportIsNotNumericError, PassportIsInvalidError, PassportNotFoundError) as e:
        service_logger.warning(e)
        return False

    try:
        passport = normalize_passport(passport)
        debt = await fetch_user_debt(connection, passport)

        if debt is None:
            service_logger.warning(f"Не удалось получить долг пользователя {passport}")
            return False

        new_debt = debt - new_payment.amount

        await apply_user_payment(connection, new_payment, new_debt, passport)
        service_logger.info(f"Оплата для {passport} прошла успешно")
        return True

    except ValueError as e:
        service_logger.exception(f"Введён неверный тип данных в параметр new_payment: {e}")
        return False


async def get_debt(connection: Connection, passport: str) -> float | bool:
    """
    Сервис для получения информации о текущей задолженности пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - float: Текущий долг пользователя, если он есть.
     - bool: False, если долг отсутствует или произошла ошибка.
    """

    try:
        await validate_passport(connection, passport)
    except (PassportIsNotNumericError, PassportIsInvalidError, PassportNotFoundError) as e:
        service_logger.warning(e)
        return False

    try:
        passport = normalize_passport(passport)
        debt = await fetch_user_debt(connection, passport)
        return debt if debt is not None else False

    except Exception as e:
        service_logger.exception(f"Ошибка при попытке отобразить данные о задолженности: {e}")
        return False
