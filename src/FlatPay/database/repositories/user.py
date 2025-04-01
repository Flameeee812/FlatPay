from aiosqlite import Connection

from FlatPay.exceptions.exceptions import PassportNotFoundError


async def register_passport_to_db(connection: Connection, passport: str) -> None:
    """
    Репозиторий для регистрации пользователя в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.
    """

    await connection.execute(
        """
        INSERT INTO Taxpayers (passport) VALUES (?)
        """, (passport,)
    )
    await connection.commit()


async def remove_passport_from_db(connection: Connection, passport: str) -> None:
    """
    Репозиторий для удаления пользователя из базы данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - bool: True, если пользователь был найден и удалён; False, если пользователь не существует.
    """

    await connection.execute(
        """
        DELETE FROM Taxpayers 
        WHERE passport = ?
        """, (passport,))
    await connection.commit()


async def fetch_user_passport(connection: Connection, passport: str) -> tuple | None:
    """
    Репозиторий для получения номера паспорта пользователя из базы данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Паспортные данные пользователя.

    Возвращает:
     - str | None: Паспорт, если найден, иначе None.
    """

    async with connection.execute(
            """
            SELECT passport 
            FROM Taxpayers 
            WHERE passport = ?
            """, (passport,)
    ) as cursor:
        passport = await cursor.fetchone()

    return passport
