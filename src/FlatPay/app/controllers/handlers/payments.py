import quart as qa
from quart import g
from aiosqlite import Connection

from FlatPay.services.payments import apply_payment, get_debt
from FlatPay.app.models.models import NewPayment


async def apply_user_payment() -> str:
    """
    Хендлер для страницы оплаты задолженности.

    В случае GET-запроса возвращает страницу с формой для оплаты задолженности.
    В случае POST-запроса пытается обработать оплату задолженности пользователя по номеру паспорта.
    Если оплата прошла успешно, отображается страница с подтверждением оплаты, иначе ошибка.
    """

    if qa.request.method == "GET":
        return await qa.render_template("update_debt.html")

    elif qa.request.method == "POST":
        form_data: dict = await qa.request.form
        passport: str = form_data.get("passport")
        new_payment: NewPayment = NewPayment(amount=form_data.get("new_payment"))

        db_conn: Connection = g.db_conn
        if await apply_payment(db_conn, passport, new_payment) is not False:
            return await qa.render_template("successful_update_debt.html", passport=passport)

        return await qa.render_template("lose_update_debt.html")


async def get_debt_info() -> str:
    """
    Хендлер для страницы получения информации о задолженности.

    В случае GET-запроса возвращает страницу с формой для получения информации о задолженности.
    В случае POST-запроса пытается получить информацию о задолженности пользователя по номеру паспорта.
    Если данные о задолженности получены успешно, отображается страница с информацией о задолженности, иначе ошибка.
    """

    if qa.request.method == "GET":
        return await qa.render_template("get_debt.html")

    elif qa.request.method == "POST":
        form_data: dict = await qa.request.form
        passport: str = form_data.get("passport")

        db_conn: Connection = g.db_conn
        new_debt: str | bool = await get_debt(db_conn, passport)
        if new_debt is not False:
            return await qa.render_template("successful_get_debt.html",
                                            passport=passport,
                                            new_debt=new_debt)

        return await qa.render_template("lose_get_debt.html")
