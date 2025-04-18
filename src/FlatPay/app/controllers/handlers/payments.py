import quart as qa
from quart import g, session
from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.services.payments import apply_payment, get_current_debt
from FlatPay.app.models.models import Payment


async def apply_user_payment() -> str:
    """
    Обработчик страницы оплаты задолженности.

    GET-запрос:
     - Отображает страницу с формой для оплаты задолженности.

    POST-запрос:
     - Пытается обработать оплату задолженности пользователя.
     - Если оплата прошла успешно, отображает страницу с подтверждением, иначе — ошибку.

    Возвращаемое значение:
     - str: HTML-страница с оповещением об успешной оплате или ошибке.
    """

    request = qa.request
    # Получаем соединение с базой данных
    connection: Connection = g.db_conn
    # Получаем email пользователя из сессии
    email: EmailStr = session.get("user_email")

    if request.method == "GET":
        # Возвращаем страницу с формой для оплаты задолженности
        return await qa.render_template("apply_payment.html")

    elif request.method == "POST":
        form_data: dict = await request.form  # Получаем данные из формы
        new_payment: Payment = Payment(amount=form_data.get("new_payment"))  # Создаём объект платежа

        try:
            # Применяем платёж и обновляем данные пользователя в БД
            await apply_payment(connection, email, new_payment)
            # Если оплата успешна, возвращаем страницу с подтверждением
            return await qa.render_template("successful_apply_payment.html", email=email)

        except ValueError:
            # В случае ошибки при попытке оплаты, возвращаем страницу с ошибкой
            return await qa.render_template("lose_update_debt.html")


async def get_user_current_debt() -> str | None:
    """
    Обработчик страницы получения информации о задолженности.

    GET-запрос:
     - Отображает страницу с формой для получения информации о задолженности.

    POST-запрос:
     - Получает информацию о задолженности пользователя.
     - Если данные получены успешно, отображает страницу с информацией о задолженности, иначе — ошибку.

    Возвращаемое значение:
     - str: HTML-страница с результатом или ошибкой.
    """

    # Обрабатываем только GET-запрос
    request = qa.request
    # Получаем соединение с базой данных
    connection: Connection = g.db_conn
    # Получаем email пользователя из сессии
    email: EmailStr = session.get("user_email")

    if request.method == "GET":
        # Получаем текущую задолженность пользователя
        current_debt: float = await get_current_debt(connection, email)

        if current_debt is not False:
            # Если задолженность найдена, возвращаем страницу с информацией о задолженности
            return await qa.render_template("get_current_month_debt.html",
                                            email=email,
                                            current_debt=current_debt)

        # Если задолженность не найдена, возвращаем страницу с ошибкой
        return await qa.render_template("lose_get_debt.html")
