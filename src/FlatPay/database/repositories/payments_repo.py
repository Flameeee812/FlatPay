from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.app.models import Payment


async def update_current_month_debt_repo(connection: Connection) -> None:
    """
    Репозиторий для обновления долга за текущий месяц:
    складывает current_month_debt и next_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET debt = current_month_debt + next_month_debt
        """
    )

    await connection.commit()


async def reset_next_month_debt_repo(connection: Connection) -> None:
    """
    Репозиторий для сброса долга в столбце next_month_debt.

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


async def update_next_month_debt_repo(connection: Connection, debt: float, email: EmailStr) -> None:
    """
    Репозиторий для обновления долга пользователя за следующий месяц.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - debt (float): Долг, который нужно установить на следующий месяц.
     - email (EmailStr): Электронная почта пользователя.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET next_month_debt = ? 
        WHERE email = ?
        """, (debt, email)
    )

    await connection.commit()


async def apply_user_payment_repo(
        connection: Connection, new_payment: Payment, new_debt: float, email: EmailStr
) -> None:
    """
    Репозиторий для оплаты задолжности пользователя.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - new_payment (NewPayment): Данные о новом платеже.
     - new_debt (float): Новый долг после учёта платежа.
     - email (EmailStr): Электронная почта пользователя.
    """

    await connection.execute(
        """
        UPDATE Taxpayers 
        SET last_payment = ?, current_month_debt = ? 
        WHERE email = ?
        """, (new_payment.amount, new_debt, email)
    )

    await connection.commit()


async def fetch_current_debt_repo(connection: Connection, email: EmailStr) -> float:
    """
    Репозиторий для извлечения долга пользователя из столбца current_month_debt.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.

    Возвращаемое значение:
     - float: Текущий долг пользователя.
    """

    async with connection.execute(
            """
            SELECT current_month_debt 
            FROM Taxpayers 
            WHERE email = ?
            """, (email,)
    ) as cursor:
        current_debt = await cursor.fetchone()

    return current_debt[0]
