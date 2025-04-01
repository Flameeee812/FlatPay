import logging
from sqlite3 import Connection, IntegrityError

from FlatPay.database.repositories.user import register_passport_to_db, remove_passport_from_db
from FlatPay.utils.validators import validate_passport, is_valid_passport, is_passport_numeric
from FlatPay.exceptions import PassportNotFoundError, PassportIsNotNumericError, PassportIsInvalidError


service_logger = logging.getLogger("user")


async def register_passport(connection: Connection, passport: str) -> bool:
    """
    Сервис для регистрации нового пользователя в базе данных.

    Перед добавлением выполняется проверка корректности введённых паспортных данных.

    Параметры:
     - connection (Connection): Подключение к базе данных.
     - passport (str): Паспортные данные пользователя.

    Возвращаемое значение:
     - bool: True, если регистрация прошла успешно, иначе False.
    """

    try:
        is_passport_numeric(passport)
    except PassportIsNotNumericError as e:
        service_logger.warning(e)
        return False

    try:
        is_valid_passport(passport)
    except PassportIsInvalidError as e:
        service_logger.warning(e)
        return False

    try:
        await register_passport_to_db(connection, passport)
        service_logger.info(f"Пользователь {passport} успешно добавлен")
        return True

    except IntegrityError as e:
        service_logger.error(f"Ошибка целостности данных: {e}")
        return False

    except Exception as e:
        service_logger.error(f"Ошибка при добавлении пользователя: {e}")
        return False


async def remove_passport(connection: Connection, passport: str) -> bool:
    """
    Сервис для удаления пользователя из базы данных.

    Перед удалением проверяется корректность паспортных данных.
    Если пользователь не найден, записывается предупреждение в лог.

    Параметры:
     - connection (Connection): Подключение к базе данных.
     - passport (str): Паспортные данные пользователя.

    Возвращаемое значение:
     - bool: True, если пользователь успешно удалён, иначе False.
    """

    try:
        await validate_passport(connection, passport)
    except (PassportIsNotNumericError, PassportIsInvalidError, PassportNotFoundError) as e:
        service_logger.warning(e)
        return False

    try:
        await remove_passport_from_db(connection, passport)
        service_logger.info(f"Пользователь {passport} удалён из базы.")
        return True

    except Exception as e:
        service_logger.warning(f"Ошибка при удалении пользователя {e}")
        return False

