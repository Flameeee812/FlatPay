from datetime import date

from quart import session
from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.database.repositories.user_repo import fetch_user_password_repo, fetch_password_salt_repo
from FlatPay.utils.security import hash_password


async def is_correct_password(connection: Connection, email: EmailStr, input_password: str) -> None | bool:
    """
    Функция для сравнения введенного пароля с хешированным паролем в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.
     - input_password (str): Введенный пользователем пароль.

    Возвращаемое значение:
     - bool | None: Возвращает True, если пароли совпадают, False, если не совпадают,
                    или None, если пользователь не найден.
    """

    # Получаем хеш пароля, сохранённый в БД
    stored_password = await fetch_user_password_repo(connection, email)

    # Получаем соль пользователя из БД (в hex-формате)
    salt = await fetch_password_salt_repo(connection, email)

    # Преобразуем соль из hex в байты
    salt = bytes.fromhex(salt)

    # Хешируем введённый пользователем пароль с солью
    hashed_input_password = hash_password(input_password, salt)

    # Сравниваем хеши — возвращаем результат сравнения
    return hashed_input_password == stored_password


def is_authenticated():
    """
    Проверяет, авторизован ли пользователь по сессии.

    Возвращает:
     - True, если пользователь вошёл в систему (session['logged_in'] == True)
     - False — если не вошёл
    """

    return session.get("logged_in") is True


def is_early(deadline: int = 12) -> bool:
    """
    Проверяет, можно ли вносить показания счётчиков на текущий день.

    Внесение запрещено, если текущая дата больше `deadline`.

    Параметры:
     - deadline (int): Последний день месяца, ДО которого разрешено внесение (по умолчанию 12).

    Возвращаемые значения:
     - bool: False — если текущий день > deadline (ввод запрещён),
             True — если день в пределах допустимого окна.
    """

    # Проверяем, превышает ли сегодняшнее число допустимый порог
    if date.today().day > deadline:
        return False

    return True
