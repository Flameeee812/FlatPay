from aiosqlite import Connection

from ..db_utils.payment_utils import calculate_base_debt


# ------------------------------------- #
async def reset_meter_readings(connection: Connection) -> None:
    """"""

    await connection.execute("UPDATE Taxpayers SET electricity = 0, cold_water = 0, hot_water = 0, gas = 0")
    await connection.commit()

    return None


# ------------------------------------- #
async def fetch_user_readings(connection: Connection, passport: str) -> tuple:
    """"""

    async with connection.execute(
            """SELECT electricity, cold_water, hot_water, gas FROM Taxpayers WHERE passport = ?""",(passport,)
    ) as cursor:
        readings = await cursor.fetchone()
    return readings


# ------------------------------------- #
def clean_readings(readings: dict[str, str]) -> dict[str, int]:
    """"""

    cleaned_readings = {key: int(value) for key, value in readings.items()}

    return cleaned_readings


async def update_user_readings(connection: Connection, passport: str, readings: dict[str, str]) -> None:
    """"""

    readings = clean_readings(readings)
    debt = calculate_base_debt(readings)

    await connection.execute("""
            UPDATE Taxpayers 
            SET electricity = ?, cold_water = ?, hot_water = ?, gas = ?, debt = ?
            WHERE passport = ?
        """, (
            readings["electricity"],
            readings["cold_water"],
            readings["hot_water"],
            readings["gas"], debt, passport
        )
                       )
    await connection.commit()

    return None
