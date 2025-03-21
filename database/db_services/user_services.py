import logging
from sqlite3 import Connection, IntegrityError

from ..db_utils.user_utils import register_passport_to_db, remove_passport_from_db
from ..db_utils.validation_utils import is_valid_passport, is_passport_numeric


service_logger = logging.getLogger("user_services")


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

    if is_valid_passport(passport) is False:
        return False

    if is_passport_numeric(passport) is False:
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


async def delete_passport(connection: Connection, passport: str) -> bool:
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

    if is_passport_numeric(passport) is False:
        return False

    try:
        result = await remove_passport_from_db(connection, passport)
        if result is True:
            service_logger.info(f"Пользователь {passport} удалён из базы.")
            return True

        service_logger.warning(f"Попытка удалить несуществующего пользователя: {passport}")
        return False

    except Exception as e:
        service_logger.warning(f"Ошибка при удалении пользователя: {e}")
        return False
