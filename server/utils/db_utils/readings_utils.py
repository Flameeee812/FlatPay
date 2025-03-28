from aiosqlite import Connection


async def reset_meter_readings(connection: Connection) -> None:
    """
    Утилита для сброса показаний счётчиков.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute("UPDATE Taxpayers SET electricity = 0, cold_water = 0, hot_water = 0, gas = 0")
    await connection.commit()

    return None


async def fetch_user_readings(connection: Connection, passport: str) -> tuple:
    """
    Утилита для получения показаний счётчиков пользователя по его паспорту.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - tuple: Кортеж с показаниями (electricity, cold_water, hot_water, gas).
    """

    async with connection.execute(
            """SELECT electricity, cold_water, hot_water, gas FROM Taxpayers WHERE passport = ?""", (passport,)
    ) as cursor:
        readings = await cursor.fetchone()
    return readings


def clean_readings(readings: dict[str, str]) -> dict[str, int]:
    """
    Утилита для конвертирования значений показаний счётчиков из строки в число.

    Параметры;
     - readings (dict[str, str]): Словарь с показаниями в виде строк.

    Возвращаемое значение:
     - dict[str, int]: Словарь со значениями, преобразованными в целочисленный формат.
    """

    cleaned_readings = {}
    for key, value in readings.items():
        try:
            cleaned_readings[key] = int(value)
        except ValueError:
            cleaned_readings[key] = 0

    return cleaned_readings


async def update_user_readings(connection: Connection, passport: str, readings: dict[str, str]) -> None:
    """
    Утилита, обновляющая показания счетчиков пользователя в базе данных.


    Параметры
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.
     - readings (dict): Словарь с показаниями для различных ресурсов (электричество, вода, газ).
    """

    readings = clean_readings(readings)

    await connection.execute(
        """UPDATE Taxpayers SET electricity = ?, cold_water = ?, hot_water = ?, gas = ? WHERE passport = ?""",
        (readings["electricity"],
         readings["cold_water"],
         readings["hot_water"],
         readings["gas"],
         passport)
                             )
    await connection.commit()

    return None
