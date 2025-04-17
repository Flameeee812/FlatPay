import logging

from aiosqlite import Connection, IntegrityError
from pydantic import EmailStr

from FlatPay.database.repositories.user_repo import register_user_repo


# Инициализируем логирование
logger = logging.getLogger("user_services")


async def register_user(connection: Connection, email: EmailStr, password: str) -> bool:
    """
    Сервис для регистрации нового пользователя в базе данных.

    Выполняет проверку корректности данных перед добавлением пользователя
    в базу данных.

    Параметры:
     - connection (Connection): Подключение к базе данных.
     - email (EmailStr): Электронная почта пользователя.
     - password (str): Пароль пользователя.

    Возвращаемое значение:
     - bool: True, если регистрация прошла успешно; False в случае ошибки.
    """

    try:
        # Регистрируем пользователя в системе
        await register_user_repo(connection, email, password)
        logger.info(f"Пользователь {email} успешно добавлен.")
        return True

    except IntegrityError as e:
        logger.error(f"Ошибка целостности данных: {e}")
        return False

    except Exception as e:
        logger.exception(f"Ошибка при добавлении пользователя: {e}")
        return False
