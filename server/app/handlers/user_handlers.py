import quart as qa
from quart import g
from aiosqlite import Connection

from server.services.db_services import user_services


async def home_handler() -> str:
    """
    Хендлер для домашней страницы.

    - Возвращает страницу домашней страницы сайта.
    """

    return await qa.render_template("home.html")


async def registration() -> str:
    """
    Хендлер для страницы регистрации пользователя.

    - В случае GET-запроса возвращает страницу с формой для регистрации пользователя.
    - В случае POST-запроса пытается зарегистрировать пользователя в базе данных по номеру паспорта.
    - Если регистрация успешна, отображается страница подтверждения регистрации, иначе ошибка.
    """

    if qa.request.method == "GET":
        return await qa.render_template("reg_user.html")

    elif qa.request.method == "POST":
        form_data: dict = await qa.request.form
        passport: str = form_data.get("passport")

        db_conn: Connection = g.db_conn
        if await user_services.register_passport(db_conn, passport):
            return await qa.render_template("successful_reg.html", passport=passport)

        return await qa.render_template("lose_reg.html")


async def delete_user_passport() -> str:
    """
    Хендлер для страницы удаления пользователя.

    - В случае GET-запроса возвращает страницу с формой для удаления пользователя.
    - В случае POST-запроса пытается удалить пользователя из базы данных по номеру паспорта.
    - Если удаление прошло успешно, отображается страница с подтверждением, иначе ошибка.
    """

    if qa.request.method == "GET":
        return await qa.render_template("del_user.html")

    elif qa.request.method == "POST":
        form_data: dict = await qa.request.form
        passport: str = form_data.get("passport")

        db_conn: Connection = g.db_conn
        if await user_services.delete_passport(db_conn, passport):
            return await qa.render_template("successful_del.html", passport=passport)

        return await qa.render_template("lose_del.html")
