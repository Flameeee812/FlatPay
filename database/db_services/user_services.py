import logging
from sqlite3 import Connection, IntegrityError

from ..db_utils.user_utils import register_passport_to_db, remove_passport_from_db
from ..db_utils.validation_utils import is_valid_passport, is_passport_numeric


service_logger = logging.getLogger("_services")


async def register_passport(connection: Connection, passport: str) -> bool:
    """Сервис для добавления пользователя в базу данных

    Параметры:
    1. connection - подключение к базе данных
    2. passport - паспортные данные пользователя
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
    """Функция для удаления пользователя из базы данных

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
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
