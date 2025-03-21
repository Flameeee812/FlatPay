from aiosqlite import Connection

from ..db_utils.validation_utils import is_user_exists


async def register_passport_to_db(connection: Connection, passport: str) -> None:
    """"""

    await connection.execute("""INSERT INTO Taxpayers (passport) VALUES (?)""", (passport,))

    await connection.commit()
    return None


async def remove_passport_from_db(connection: Connection, passport: str) -> bool:
    """"""

    result = await is_user_exists(connection, passport)
    if result is True:
        await connection.execute("DELETE FROM Taxpayers WHERE passport = ?", (passport,))
        await connection.commit()
        return True

    return False
