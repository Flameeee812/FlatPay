from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.utils.security import hash_password


async def register_user_repo(connection: Connection, email: EmailStr, password: str) -> None:
    """
    Репозиторий для регистрации пользователя в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.
     - password (str): Пароль пользователя.
    """

    hashed_password, salt = hash_password(password)

    await connection.execute(
        """
        INSERT INTO Taxpayers (email, password, salt) VALUES (?, ?, ?)
        """, (email, hashed_password, salt)
    )
    await connection.commit()


async def fetch_user_password_repo(connection: Connection, email: EmailStr) -> str | None:
    """
    Репозиторий для получения хешированного пароля пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.

    Возвращаемое значение:
     - str | None: Хешированный пароль пользователя, если он найден; иначе None.
    """

    async with connection.execute(
            """
            SELECT password
            FROM Taxpayers 
            WHERE email = ?
            """, (email, )
    ) as cursor:
        password = await cursor.fetchone()

    if password:
        return password[0]

    return None


async def fetch_password_salt_repo(connection: Connection, email: EmailStr) -> str | None:
    """
    Репозиторий для получения соли пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.

    Возвращаемое значение:
     - str | None: Соль пользователя, если она найдена; иначе None.
    """

    async with connection.execute(
            """
            SELECT salt
            FROM Taxpayers 
            WHERE email = ?
            """, (email, )
    ) as cursor:
        salt = await cursor.fetchone()

    if salt:
        return salt[0]

    return None
