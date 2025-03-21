import flask as fl
from flask import g

from database.db_services import payment_services


async def apply_user_payment():
    """Хендлер для страницы оплаты задолжности"""

    if fl.request.method == "GET":
        return fl.render_template("update_debt.html")

    elif fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        new_payment = fl.request.form.get("new_payment")
        db_conn = g.db_conn

        if await payment_services.apply_payment(db_conn, passport, new_payment) is not False:
            return fl.render_template("successful_update_debt.html", passport=passport)

        return fl.render_template("lose_update_debt.html")


async def get_debt_info():
    """Хендлер для страницы получния информации о задолжности"""

    if fl.request.method == "GET":
        return fl.render_template("get_debt.html")

    elif fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        db_conn = g.db_conn
        new_debt = await payment_services.get_debt(db_conn, passport)

        if new_debt is not False:
            return fl.render_template("successful_get_debt.html",
                                      passport=passport,
                                      new_debt=new_debt)

        return fl.render_template("lose_get_debt.html")
