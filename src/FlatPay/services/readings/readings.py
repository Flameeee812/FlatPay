import logging
from sqlite3 import Connection

from FlatPay.database.repositories.readings import (
    reset_meter_readings, update_user_readings, fetch_user_readings
)
from FlatPay.utils.validators import validate_passport
from FlatPay.app.models import Readings
from FlatPay.exceptions.exceptions import PassportIsNotNumericError, PassportNotFoundError, PassportIsInvalidError


service_logger = logging.getLogger("readings")


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


async def update_readings(connection: Connection, passport: str, readings: Readings) -> bool:
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

    try:
        await validate_passport(connection, passport)
    except (PassportIsNotNumericError, PassportIsInvalidError, PassportNotFoundError) as e:
        service_logger.warning(e)
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

    try:
        await validate_passport(connection, passport)
    except (PassportIsNotNumericError, PassportIsInvalidError, PassportNotFoundError) as e:
        service_logger.warning(e)
        return False

    try:
        result = await fetch_user_readings(connection, passport)

        if result is not None:
            service_logger.info(f"Получены данные о показаниях для пользователя: {passport}")
            return result

        service_logger.warning(f"Данные о о показания пользователя отсутствуют {result}")
        return False

    except Exception as e:
        service_logger.exception(f"Ошибка при попытке отобразить данные о показаниях: {e}")
        return False
