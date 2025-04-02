from aiosqlite import Connection

from FlatPay.app.models import NewPayment


async def update_current_month_debt(connection: Connection) -> None:
    """
    Репозиторий, обновляющий долг за текущий месяц, добавляя долг из столбца next_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET debt = debt + next_month_debt
        """
    )

    await connection.commit()


async def reset_next_month_debt(connection: Connection) -> None:
    """
    Репозиторий, сбрасывающий долг в столбце next_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET next_month_debt = 0
        """
    )

    await connection.commit()


async def update_next_month_debt(connection: Connection, debt: float, passport: str) -> None:
    """
    Репозиторий, обновляющий долг за следующий месяц для указанного пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - debt (float): Долг, который нужно установить на следующий месяц.
     - passport (str): Номер паспорта пользователя.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET next_month_debt = ? 
        WHERE passport = ?
        """, (debt, passport)
    )

    await connection.commit()


async def apply_user_payment(connection: Connection, new_payment: NewPayment, new_debt: float, passport: str) -> None:
    """
    Репозиторий, применяющаий оплату пользователя, обновляя данные о платеже и долге.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - new_payment (float): Сумма нового платежа.
     - new_debt (float): Новый долг после учета платежа.
     - passport (str): Номер паспорта пользователя.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET last_payment = ?, debt = ? 
        WHERE passport = ?
        """, (new_payment.amount, new_debt, passport)
    )

    await connection.commit()
    return None


async def fetch_user_debt(connection: Connection, passport: str) -> float:
    """
    Репозиторий, извлекающий текущий долг пользователя из базы данных.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - passport (str): Номер паспорта пользователя.

    Возвращаемое значение:
     - float: Текущий долг пользователя
    """

    async with connection.execute(
            """
            SELECT debt 
            FROM Taxpayers 
            WHERE passport = ?
            """, (passport,)
    ) as cursor:
        debt = await cursor.fetchone()

    current_debt = debt[0]

    if current_debt != 0:
        return round(current_debt, 2)

    return 0.0
