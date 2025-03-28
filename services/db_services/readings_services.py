import logging
from sqlite3 import Connection

from utils.db_utils.readings_utils import (
    reset_meter_readings, update_user_readings, fetch_user_readings
)
from utils.validation_utils import is_user_exists, is_passport_numeric


service_logger = logging.getLogger("readings_services")


async def reset_readings(connection: Connection) -> None:
    """
    Сервис для обнуления показаний счётчиков всех пользователей.

    Параметры:
     - connection (Connection): Подключение к базе данных.
    """

    try:
        await reset_meter_readings(connection)
        service_logger.info("Столбцы с показаниями счётчиков обнулились")

    except Exception as e:
        service_logger.exception(f"Ошибка при обновлении долга: {e}")
        return None


async def update_readings(connection: Connection, passport: str, readings: dict[str, str]) -> bool:
    """
    Сервис для обновления показаний счётчиков пользователя.

    Перед обновлением выполняется проверка существования пользователя
    и корректности переданных паспортных данных.

    Параметры:
     - connection (Connection): Подключение к базе данных.
     - passport (str): Паспортные данные пользователя.
     - readings (dict[str, str]): Новые показания счётчиков в формате {тип_ресурса: расход}.

    Возвращаемое значение:
     - bool: True, если обновление прошло успешно, иначе False.
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
        service_logger. exception(f"Ошибка при добавлении показаний в базу данных: {e}")
        return False


async def get_readings(connection: Connection, passport: str) -> tuple | bool:
    """
    Сервис для получения актуальных показаний счётчиков пользователя.

    Перед запросом проверяется корректность паспортных данных.

    Параметры:
    - connection (Connection): Подключение к базе данных.
    - passport (str): Паспортные данные пользователя.

    Возвращаемое значение:
     - tuple: Кортеж с показаниями счётчиков, если данные найдены.
     - bool: False, если пользователь не найден или произошла ошибка.
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
