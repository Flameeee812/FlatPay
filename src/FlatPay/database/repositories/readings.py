from aiosqlite import Connection

from FlatPay.app.models.models import Readings


async def reset_meter_readings(connection: Connection) -> None:
    """
    Репозиторий для сброса показаний счётчиков.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET electricity = 0, cold_water = 0, hot_water = 0, gas = 0
        """
    )
    await connection.commit()


async def fetch_user_readings(connection: Connection, passport: str) -> tuple:
    """
    Репозиторий для получения показаний счётчиков пользователя по его паспорту.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - tuple: Кортеж с показаниями (electricity, cold_water, hot_water, gas).
    """

    async with connection.execute(
            """
            SELECT electricity, cold_water, hot_water, gas 
            FROM Taxpayers 
            WHERE passport = ?
            """, (passport,)
    ) as cursor:
        readings = await cursor.fetchone()
    return readings


async def update_user_readings(connection: Connection, passport: str, readings: Readings) -> None:
    """
    Репозиторий, обновляющий показания счетчиков пользователя в базе данных.


    Параметры
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.
     - readings (dict): Словарь с показаниями для различных ресурсов (электричество, вода, газ).
    """

    await connection.execute(
        """UPDATE Taxpayers 
        SET electricity = ?, cold_water = ?, hot_water = ?, gas = ? 
        WHERE passport = ?
        """, (readings.meter_readings["electricity"],
              readings.meter_readings["cold_water"],
              readings.meter_readings["hot_water"],
              readings.meter_readings["gas"],
              passport)
    )
    await connection.commit()
