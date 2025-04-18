import logging

from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.database.repositories.payments_repo import (
    apply_user_payment_repo,  fetch_current_debt_repo
)
from FlatPay.app.models import Payment


# Инициализируем логирование
logger = logging.getLogger("payments_services")


async def apply_payment(connection: Connection, email: EmailStr, payment: Payment) -> bool:
    """
    Сервис для применения оплаты и обновления текущей задолженности.

    Вычитает сумму оплаты из текущего долга и сохраняет новое значение.

    Параметры:
     - connection (Connection): Асинхронное соединение с базой данных.
     - email (EmailStr): Электронная почта пользователя.
     - new_payment (NewPayment): Данные об оплате.

    Возвращаемое значение:
     - bool: True, если оплата успешно применена, иначе False.
    """

    try:
        # Получаем значение из столбца current_month_debt
        current_month_debt: float = await fetch_current_debt_repo(connection, email)

        # Высчитываем остаток долга за текущий месяц
        new_debt = current_month_debt - payment.amount

        # Передаем значение new_debt в столбец current_month_debt
        await apply_user_payment_repo(connection, payment, new_debt, email)
        logger.info(f"Оплата для {email} прошла успешно")
        return True

    except ValueError as e:
        logger.exception(f"Введён неверный тип данных в параметр new_payment: {e}")
        return False
