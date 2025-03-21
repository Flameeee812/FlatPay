import logging

from aiosqlite import Connection


utils_logger = logging.getLogger("validation_utils")


def is_passport_numeric(passport):
    """Функция для проверки того, что все переданные символы являются чисоами."""

    if all(char.isdigit() for char in passport.split()) is False:
        utils_logger.error(f"Введён неверный тип данных: {passport}")
        return False

    return True


async def is_user_exists(connection: Connection, passport: str) -> bool:
    """Проверяет, существует ли пользователь с данным паспортом в базе данных."""

    async with connection.execute("SELECT passport FROM Taxpayers WHERE passport = ?", (passport,)) as cursor:
        passport = await cursor.fetchone()

    return passport is not None and passport[0] is not None


def is_valid_passport(passport):
    """Функция для проверки валидности переданных паспортных данных."""

    if (len("".join(passport.split())) != 10) or (len(passport.split()) != 2):
        utils_logger.error(f"Неверное заполнение паспортных данных: {passport}")
        return False

    return True
