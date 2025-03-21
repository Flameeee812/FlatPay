import logging
from sqlite3 import Connection

from ..db_utils.readings_utils import (
    reset_meter_readings, update_user_readings, fetch_user_readings
)
from ..db_utils.validation_utils import is_user_exists, is_passport_numeric


service_logger = logging.getLogger("readings_services")


async def reset_readings(connection: Connection) -> None:
    """Функция, обнуляющая показания счетчиков.

    Параметры:
    1. connection - подключение к базе данных
    """

    try:
        await reset_meter_readings(connection)
        service_logger.info("Столбцы с показаниями счётчиков обнулились")

    except Exception as e:
        service_logger.exception(f"Ошибка при обновлении долга: {e}")
        return None


async def update_readings(connection: Connection, passport: str, readings: dict[str, str]) -> bool:
    """Функция для обновления показаний счётчиков пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
        3. readings -
        """

    if await is_user_exists(connection, passport) is False:
        return False

    if is_passport_numeric(passport) is False:
        return False

    try:
        await update_user_readings(connection, passport, readings)
        service_logger.info(f"Показания для пользователя {passport} успешно обновлены.")
        return True

    except Exception as e:
        service_logger.exception(f"Ошибка при добавлении показаний в базу данных: {e}")
        return False


async def get_readings(connection: Connection, passport: str) -> tuple | bool:
    """Функция для получения информации о показаниях счётчиков пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
        """

    if is_passport_numeric(passport) is False:
        return False

    try:
        result = await fetch_user_readings(connection, passport)

        if result is not None:
            service_logger.info(f"Получены данные о показаниях для пользователя: {passport}")
            return result

        service_logger.warning(result)
        return False

    except Exception as e:
        service_logger.exception(f"Ошибка при попытке отобразить данные о показаниях: {e}")
        return False
