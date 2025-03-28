import quart as qa
from quart import g
from aiosqlite import Connection

from server.services.db_services import readings_services
from server.services.db_services.payment_services import update_next_debt
from server.utils.validation_utils import is_early


async def update_user_readings() -> str:
    """
    Хендлер для обработки запросов для обновления показаний счётчиков пользователя.

    - В случае GET-запроса возвращает страницу с формой для обновления данных.
    - В случае POST-запроса обновляет показания счётчиков в базе данных и, если обновление прошло успешно,
      вызывает обновление долга пользователя. Затем возвращает страницу с подтверждением или ошибкой.

    Параметры:
    Нет.

    Возвращаемое значение:
    - Шаблон страницы с результатом обновления показаний счётчиков (успех или ошибка).
    """
    if qa.request.method == "GET":
        return await qa.render_template("update_readings.html")

    elif qa.request.method == "POST":
        form_data: dict = await qa.request.form
        passport: str = form_data.get("passport")
        readings = {
            "electricity": form_data.get("electricity"),
            "cold_water": form_data.get("cold_water"),
            "hot_water": form_data.get("hot_water"),
            "gas": form_data.get("gas")
        }

        db_conn: Connection = g.db_conn
        if is_early(passport):
            return await qa.render_template("early_update_readings.html")

        if await readings_services.update_readings(db_conn, passport, readings):
            await update_next_debt(db_conn, passport, readings)
            return await qa.render_template("successful_update_readings.html", passport=passport)

        return await qa.render_template("lose_update_readings.html")


async def get_readings_info() -> str:
    """
    Хендлер для обработки запросов для получения информации о показаниях счётчиков пользователя.

    - В случае GET-запроса возвращает страницу с формой для получения данных.
    - В случае POST-запроса извлекает показания из базы данных и отображает их пользователю.
    - Если данные о показаниях не найдены, возвращается ошибка.

    Параметры:
    Нет.

    Возвращаемое значение:
    - Шаблон страницы с результатами получения показаний счётчиков (успех или ошибка).
    """
    if qa.request.method == "GET":
        return await qa.render_template("get_readings.html")

    elif qa.request.method == "POST":
        form_data: dict = await qa.request.form
        passport: str = form_data.get("passport")

        db_conn: Connection = g.db_conn
        readings: tuple | bool = await readings_services.get_readings(db_conn, passport)

        if readings is not False:
            return await qa.render_template("successful_get_readings.html",
                                            passport=passport,
                                            electricity=readings[0],
                                            cold_water=readings[1],
                                            hot_water=readings[2],
                                            gas=readings[3])

        return await qa.render_template("lose_get_readings.html")
