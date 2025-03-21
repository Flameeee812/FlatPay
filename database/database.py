import os

import aiosqlite as sql

from config import load_config
from logger import setup_logger


config = load_config()


async def get_connection():
    """Функция для получения базы данных"""

    connection = await sql.connect(config.DATABASE_PATH, check_same_thread=False)

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
        last_month_debt REAL DEFAULT 0.0
    )
    ''')

    await connection.commit()

    return connection


def close_connection(connection):
    """Функция для закрытия базы данных.

    Параметры:
    1. connection - подключение к базе данных
    """

    connection.close()
    logger.app_logger.info("База данных закрыта")

    return None
