from aiosqlite import Connection

from .readings_utils import clean_readings


async def update_current_month_debt(connection: Connection) -> None:
    """
    Утилита, обновляющая долг за текущий месяц, добавляя долг из столбца next_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute("UPDATE Taxpayers SET debt = debt + next_month_debt")

    await connection.commit()
    return None


async def reset_next_month_debt(connection: Connection) -> None:
    """
    Утилита, сбрасывающая долг в столбце next_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute("UPDATE Taxpayers SET next_month_debt = 0")

    await connection.commit()
    return None


def calculate_base_debt(readings: dict[str, str]) -> float:
    """
    Утилита для подсчёта долга по актуальному Казансому тарифу.

    Параметры:
     - readings (dict): Словарь с показаниями для различных ресурсов (электричество, вода, газ).

    Возвращаемое значение:
     - float: Рассчитанный долг по актуальному тарифу.
    """

    tariffs = {
        "electricity": 5.09,
        "cold_water": 29.41,
        "hot_water": 226.7,
        "gas": 7.47}
    base_debt = 0.0
    readings = clean_readings(readings)

    for key, rate in tariffs.items():
        base_debt += readings[key] * rate
    return round(base_debt, 2)


async def update_next_month_debt(connection: Connection, debt: float, passport: str) -> None:
    """
    Утилита, обновляющая долг за следующий месяц для указанного пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - debt (float): Долг, который нужно установить на следующий месяц.
     - passport (str): Номер паспорта пользователя.
    """

    await connection.execute(
        "UPDATE Taxpayers SET next_month_debt = ? WHERE passport = ?", (debt, passport)
    )

    await connection.commit()
    return None


async def apply_user_payment(connection: Connection, new_payment: float, new_debt: float, passport: str) -> None:
    """
    Утилита, применяющая оплату пользователя, обновляя данные о платеже и долге.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - new_payment (float): Сумма нового платежа.
     - new_debt (float): Новый долг после учета платежа.
     - passport (str): Номер паспорта пользователя.
    """

    await connection.execute(
        """UPDATE Taxpayers SET last_payment = ?, debt = ? WHERE passport = ?""", (new_payment, new_debt, passport)
    )

    await connection.commit()
    return None


async def fetch_user_debt(connection: Connection, passport: str) -> float:
    """
    Утилита, извлекающая текущий долг пользователя из базы данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - float: Текущий долг пользователя
    """

    async with connection.execute(
            "SELECT debt FROM Taxpayers WHERE passport = ?", (passport,)
    ) as cursor:
        debt = await cursor.fetchone()

    current_debt = debt[0]

    if current_debt != 0:
        return round(current_debt, 2)

    return 0.0
