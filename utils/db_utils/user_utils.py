from aiosqlite import Connection

from utils.validation_utils import is_user_exists


async def register_passport_to_db(connection: Connection, passport: str) -> None:
    """
    Утилита для регистрации пользователя в базе данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.
    """

    await connection.execute("""INSERT INTO Taxpayers (passport) VALUES (?)""", (passport,))

    await connection.commit()
    return None


async def remove_passport_from_db(connection: Connection, passport: str) -> bool:
    """
    Утилита для удаления пользователя из базы данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - bool: True, если пользователь был найден и удалён; False, если пользователь не существует.
    """

    result = await is_user_exists(connection, passport)
    if result is True:
        await connection.execute("DELETE FROM Taxpayers WHERE passport = ?", (passport,))
        await connection.commit()
        return True

    return False
