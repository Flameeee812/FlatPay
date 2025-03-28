import flask as fl
from flask import g

from server.services.db_services import user_services


async def home_handler():
    """
    Хендлер для домашней страницы.

    - Возвращает страницу домашней страницы сайта.
    """

    return fl.render_template("home.html")


async def registration():
    """
    Хендлер для страницы регистрации пользователя.

    - В случае GET-запроса возвращает страницу с формой для регистрации пользователя.
    - В случае POST-запроса пытается зарегистрировать пользователя в базе данных по номеру паспорта.
    - Если регистрация успешна, отображается страница подтверждения регистрации, иначе ошибка.
    """

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
    """
    Хендлер для страницы удаления пользователя.

    - В случае GET-запроса возвращает страницу с формой для удаления пользователя.
    - В случае POST-запроса пытается удалить пользователя из базы данных по номеру паспорта.
    - Если удаление прошло успешно, отображается страница с подтверждением, иначе ошибка.
    """

    if fl.request.method == "GET":
        return fl.render_template("del_user.html")

    elif fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        db_conn = g.db_conn

        if await user_services.delete_passport(db_conn, passport):
            return fl.render_template("successful_del.html", passport=passport)

        return fl.render_template("lose_del.html")
