from aiosqlite import Connection


# ------------------------------------- #
async def archive_debt_to_last_month(connection: Connection) -> None:
    """"""

    await connection.execute("UPDATE Taxpayers SET last_month_debt = debt, debt = 0")

    await connection.commit()
    return None


# ------------------------------------- #
def calculate_base_debt(readings: dict[str, int]) -> float:
    """Функция для подсчёта долга по актуальному Казансому тарифу."""

    tariffs = {
        "electricity": 5.09,
        "cold_water": 29.41,
        "hot_water": 226.7,
        "gas": 7.47}
    base_debt = 0.0

    for key, rate in tariffs.items():
        base_debt += readings[key] * rate
    return round(base_debt, 2)


# ------------------------------------- #
async def fetch_current_debt(connection: Connection, passport: str) -> float:
    """Функция для получения долга за нынешний месяц."""

    async with connection.execute("SELECT debt FROM Taxpayers WHERE passport = ?", (passport,)) as cursor:
        debt = await cursor.fetchone()[0]
    return debt


async def fetch_last_month_debt(connection: Connection, passport: str) -> float:
    """Функция для получения долга за предыдщий месяц."""

    async with connection.execute("SELECT last_month_debt FROM Taxpayers WHERE passport = ?", (passport,)) as cursor:
        last_month_debt = await cursor.fetchone()[0]
    return last_month_debt


async def calculate_actual_debt(connection: Connection, passport: str) -> float:
    """Функия для подсчёта актуального долга."""

    debt = await fetch_current_debt(connection, passport)
    last_month_debt = await fetch_last_month_debt(connection, passport)

    return debt + last_month_debt


async def update_debt_amount(connection: Connection, actual_debt: float, passport: str) -> None:
    """"""

    await connection.execute(
        "UPDATE Taxpayers SET debt = ? WHERE passport = ?", (actual_debt, passport)
    )

    await connection.commit()
    return None


# ------------------------------------- #
async def apply_user_payment(connection: Connection, new_payment: float, new_debt: float, passport: str) -> None:
    """"""

    await connection.execute(
        """UPDATE Taxpayers SET last_payment = ?, debt = ? WHERE passport = ?""", (new_payment, new_debt, passport)
    )

    await connection.commit()
    return None


# ------------------------------------- #
async def fetch_user_debt(connection, passport):
    """"""

    async with connection.execute(
            "SELECT debt, last_month_debt FROM Taxpayers WHERE passport = ?", (passport,)
    ) as cursor:
        debt = await cursor.fetchone()

    current_debt, last_month_debt = debt

    if current_debt != 0:
        return round(current_debt, 2)

    elif last_month_debt != 0:
        return round(last_month_debt, 2)

    return 0.0
