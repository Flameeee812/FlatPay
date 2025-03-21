import flask as fl
from flask import g

from database.db_services import user_services


async def home_handler():
    """Хендлер для домашней страницы"""

    return fl.render_template("home.html")


async def registration():
    """Хендлер для страницы регистрации"""

    if fl.request.method == "GET":
        return fl.render_template("reg_user.html")

    elif fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        db_conn = g.db_conn

        if await user_services.register_passport(db_conn, passport):
            return fl.render_template("successful_reg.html",
                                      passport=passport)

        return fl.render_template("lose_reg.html")


async def delete_user_passport():
    """Хендлер для страницы удаления пользователя"""

    if fl.request.method == "GET":
        return fl.render_template("del_user.html")

    elif fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        db_conn = g.db_conn

        if await user_services.delete_passport(db_conn, passport):
            return fl.render_template("successful_del.html", passport=passport)

        return fl.render_template("lose_del.html")
