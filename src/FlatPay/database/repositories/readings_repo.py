from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.app.models.models import Readings


async def reset_meter_readings_repo(connection: Connection) -> None:
    """
    Репозиторий для сброса показаний счётчиков всех пользователей.

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


async def fetch_user_readings_repo(connection: Connection, email: EmailStr) -> tuple | None:
    """
    Репозиторий для получения показаний счётчиков пользователя.

    Параметры:
    - connection (Connection): Асинхронное соединение с базой данных.
    - email (EmailStr): Электронная почта пользователя.

    Возвращаемое значение:
    - tuple | None: Кортеж с показаниями (electricity, cold_water, hot_water, gas), если данные найдены; иначе None.
    """

    async with connection.execute(
            """
            SELECT electricity, cold_water, hot_water, gas 
            FROM Taxpayers 
            WHERE email = ?
            """, (email,)
    ) as cursor:
        readings = await cursor.fetchone()

    return readings


async def update_user_readings_repo(connection: Connection, email: EmailStr, readings: Readings) -> None:
    """
    Репозиторий для обновления показаний счётчиков пользователя в базе данных.

    Параметры:
    - connection (Connection): Асинхронное соединение с базой данных.
    - email (EmailStr): Электронная почта пользователя.
    - readings (Readings): Объект Readings, содержащий новые показания счётчиков для пользователя.
    """

    await connection.execute(
        """UPDATE Taxpayers 
        SET electricity = ?, cold_water = ?, hot_water = ?, gas = ? 
        WHERE email = ?
        """, (readings.meter_readings["electricity"],
              readings.meter_readings["cold_water"],
              readings.meter_readings["hot_water"],
              readings.meter_readings["gas"],
              email)
    )
    await connection.commit()
