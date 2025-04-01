import quart as qa
from quart import g
from aiosqlite import Connection

from FlatPay.app.models import Readings
from FlatPay.services.readings import update_readings, get_readings
from FlatPay.services.payments import update_next_debt
from FlatPay.utils.validators import is_early


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
        readings = Readings(
            meter_readings={
                "electricity": form_data.get("electricity", 0) or 0,
                "cold_water": form_data.get("cold_water", 0) or 0,
                "hot_water": form_data.get("hot_water", 0) or 0,
                "gas": form_data.get("gas") or 0
            }
        )

        db_conn: Connection = g.db_conn
        if is_early():
            return await qa.render_template("early_update_readings.html")

        if await update_readings(db_conn, passport, readings):
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
        readings: tuple | bool = await get_readings(db_conn, passport)

        if readings is not False:
            return await qa.render_template("successful_get_readings.html",
                                            passport=passport,
                                            electricity=readings[0],
                                            cold_water=readings[1],
                                            hot_water=readings[2],
                                            gas=readings[3])

        return await qa.render_template("lose_get_readings.html")
