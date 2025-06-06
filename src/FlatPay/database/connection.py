import logging

from aiosqlite import Connection, connect

from FlatPay.core.exceptions import DatabaseConnectionError, DatabaseCloseError


connection_logger = logging.getLogger("connection")


async def get_connection(path: str) -> Connection:
    """
    Утилита для получения асинхронного соединения с базой данных.

    Параметры:
     - path (str): Путь к базе данных.

    Возвращаемое значение:
     - connection (Connection): Асинхронное соединение с базой данных.

    Исключения:
     - DatabaseConnectionError: Ошибка при попытке подключиться к базе данных.
    """

    try:
        # Подключаемся к базе данных асинхронно
        connection: Connection = await connect(path, check_same_thread=False)
        # Создаем таблицу, если её нет (если таблица уже есть, она не будет перезаписана)
        await create_table(connection)
        return connection

    except Exception as e:
        connection_logger.error(f"Ошибка при подключении к базе данных: {e}")
        raise DatabaseConnectionError(f"Не удалось подключиться к базе данных") from e


async def create_table(connection: Connection) -> None:
    """
    Утилита для создания таблицы `Taxpayers` в базе данных, если она не существует.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.

    Примечание:
     - Если таблица уже существует, она не будет перезаписана.
    """

    # SQL запрос для создания таблицы
    await connection.execute('''
    CREATE TABLE IF NOT EXISTS Taxpayers ( 
        email TEXT PRIMARY KEY,
        password TEXT,
        salt TEXT,
        electricity INTEGER DEFAULT 0,
        cold_water INTEGER DEFAULT 0,
        hot_water INTEGER DEFAULT 0,
        gas INTEGER DEFAULT 0,
        current_month_debt DECIMAL DEFAULT 0.0,
        last_payment DECIMAL DEFAULT 0.0,
        next_month_debt DECIMAL DEFAULT 0.0
    )
    ''')

    await connection.commit()


async def close_connection(connection: Connection) -> None:
    """
    Утилита для закрытия асинхронного соединения с базой данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.

    Исключения:
     - DatabaseCloseError: Ошибка при попытке закрыть соединение с базой данных.

    Примечание:
     - Попытка закрытия соединения будет зафиксирована в логах, если возникнут ошибки.
    """

    try:
        # Закрываем соединение с базой данных
        await connection.close()

    except Exception as e:
        connection_logger.error(f"Ошибка при попытки закрыть соединение :{e}")
        # Поднимаем исключение, чтобы вызвать обработку на более высоком уровне
        raise DatabaseCloseError("Не удалось закрыть соединение") from e

