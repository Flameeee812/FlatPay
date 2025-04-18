import logging

from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.database.repositories.payments_repo import fetch_current_debt_repo


# Инициализируем логирование
logger = logging.getLogger("payments_services")


async def get_current_debt(connection: Connection, email: EmailStr) -> float | bool:
    """
    Сервис для получения информации о текущей задолженности пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.

    Возвращаемое значение:
     - float: Текущая сумма долга, если она найдена.
     - bool: False, если произошла ошибка.
    """

    try:
        # Получаем значение из столбца current_month_debt
        current_debt = await fetch_current_debt_repo(connection, email)
        return current_debt

    except Exception as e:
        logger.exception(f"Ошибка при попытке отобразить данные о задолженности: {e}")
        return False
