import logging
from sqlite3 import Connection, IntegrityError

from FlatPay.database.repositories.user import register_passport_to_db, remove_passport_from_db
from FlatPay.utils.validators import validate_passport, is_valid_passport, is_passport_numeric
from FlatPay.utils.formatters import normalize_passport
from FlatPay.core.exceptions import PassportNotFoundError, PassportIsNotNumericError, PassportIsInvalidError


service_logger = logging.getLogger("user")


async def register_passport(connection: Connection, passport: str) -> bool:
    """
    Сервис для регистрации нового паспорта в базе данных.

    Перед добавлением выполняется проверка корректности введённых паспортных данных.
    Также производится нормализация номера, удаляя нецифровые символы.

    Параметры:
     - connection (Connection): Подключение к базе данных.
     - passport (str): Паспортные данные пользователя.

    Возвращаемое значение:
     - bool: True, если регистрация прошла успешно, иначе False.
    """

    passport = normalize_passport(passport)

    if not is_passport_numeric(passport):
        service_logger.warning(f"Паспорт содержит нецифровые символы: {passport}")
        return False

    if not is_valid_passport(passport):
        service_logger.warning(f"Некорректный номер паспорта: {passport}")
        return False

    try:
        await register_passport_to_db(connection, passport)
        service_logger.info(f"Пользователь {passport} успешно добавлен.")
        return True

    except IntegrityError as e:
        service_logger.error(f"Ошибка целостности данных: {e}")
        return False

    except Exception as e:
        service_logger.exception(f"Ошибка при добавлении пользователя: {e}")
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
        passport = normalize_passport(passport)
        await remove_passport_from_db(connection, passport)
        service_logger.info(f"Пользователь {passport} удалён из базы.")
        return True

    except Exception as e:
        service_logger.exception(f"Ошибка при удалении пользователя: {e}")
        return False
