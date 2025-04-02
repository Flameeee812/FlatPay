from datetime import date

from aiosqlite import Connection

from FlatPay.utils.formatters import normalize_passport
from FlatPay.database.repositories.user import fetch_user_passport
from FlatPay.core.exceptions import PassportIsNotNumericError, PassportIsInvalidError, PassportNotFoundError


async def validate_passport(connection: Connection, passport: str) -> None:
    """
    Проверяет корректность паспортных данных и существование пользователя в БД.

    Параметры:
    - connection (Connection): Подключение к базе данных.
    - passport (str): Паспортные данные пользователя.

    Исключения:
    - PassportIsNotNumericError: Если паспорт содержит не только цифры.
    - PassportIsInvalidError: Если паспорт не соответствует формату.
    - PassportNotFoundError: Если паспорт не найден в базе.
    """

    passport = normalize_passport(passport)
    if not is_passport_numeric(passport):
        raise PassportIsNotNumericError(f"Паспорт {passport} содержит недопустимые символы.")

    if not is_valid_passport(passport):
        raise PassportIsInvalidError(f"Паспорт {passport} не соответствует формату.")

    if await fetch_user_passport(connection, passport) is None:
        raise PassportNotFoundError(f"Пользователь с паспортом {passport} не найден.")


def is_passport_numeric(passport: str) -> bool:
    """
    Утилита для проверки того, что все переданные символы являются числами.

    Параметры:
     - passport (str): Номер паспорта пользователя.

    Возвращаемые значения:
     - bool: `True`, если паспорт содержит только цифры, иначе исключение.

    Исключения:
     - PassportIsNotNumericError: Если паспорт содержит не только цифры и пробел.
    """

    if all(char.isdigit() for char in passport.strip().split()) is False:
        raise PassportIsNotNumericError(f"Паспорт {passport} содержит недопустимые символы.")

    return True


def is_valid_passport(passport: str) -> bool:
    """
    Утиилита для проверки валидности переданных паспортных данных.

    Параметры:
     - passport (str): Номер паспорта пользователя.

    Возвращаемые значения:
     - bool: `True`, если формат корректный, иначе исключение.

    Исключения:
     - PassportIsInvalidError: Если паспорт не соответствует формату.
    """

    if (len("".join(passport.split())) != 10) and (len(passport.split()) != 2):
        raise PassportIsInvalidError(f"Паспорт {passport} не соответствует формату.")

    return True


def is_early(deadline: int = 24) -> bool:
    """
    Проверяет, можно ли вносить показания счётчиков на текущий день.

    Внесение запрещено, если текущая дата меньше `deadline`.
    В этом случае логируется попытка раннего внесения.

    Параметры:
     - deadline (int): Первый день месяца, после которого разрешено внесение (по умолчанию 24).

    Возвращаемые значения:
     - bool: `False`, если внесение запрещено, иначе `True`.
    """

    if date.today().day > deadline:
        return False

    return True
