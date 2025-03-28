from aiosqlite import Connection, connect

from ..config import config


async def get_connection():
    """
    Утилита для получения соединения с базой данных.

    Возвращаемое значение:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    connection = await connect(config.DATABASE_PATH, check_same_thread=False)
    await create_table(connection)

    return connection


async def create_table(connection: Connection):
    """
    Утилита для создания sql таблицы.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute('''
    CREATE TABLE IF NOT EXISTS Taxpayers (
        id INTEGER PRIMARY KEY,
        passport TEXT NOT NULL UNIQUE,
        electricity INTEGER DEFAULT 0,
        cold_water INTEGER DEFAULT 0,
        hot_water INTEGER DEFAULT 0,
        gas INTEGER DEFAULT 0,
        debt REAL DEFAULT 0.0,
        last_payment REAL DEFAULT 0.0,
        next_month_debt REAL DEFAULT 0.0
    )
    ''')

    await connection.commit()

    return None


def close_connection(connection: Connection):
    """Утилита для закрытия базы данных.

    Параметры:
     - connection: Асинхронное соединение с базой данных.
    """

    connection.close()
    return None
