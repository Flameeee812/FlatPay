import flask as fl
from flask import g

from services import readings_services
from services.db_services.payment_services import update_next_debt
from utils.validation_utils import is_early


async def update_user_readings():
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
    if fl.request.method == "GET":
        return fl.render_template("update_readings.html")

    elif fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        readings = {
            "electricity": fl.request.form.get("electricity"),
            "cold_water": fl.request.form.get("cold_water"),
            "hot_water": fl.request.form.get("hot_water"),
            "gas": fl.request.form.get("gas")
        }
        db_conn = g.db_conn

        if is_early(passport):
            return fl.render_template("early_update_readings.html")

        if await readings_services.update_readings(db_conn, passport, readings):
            await update_next_debt(db_conn, passport, readings)
            return fl.render_template("successful_update_readings.html", passport=passport)

        return fl.render_template("lose_update_readings.html")


async def get_readings_info():
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
    if fl.request.method == "GET":
        return fl.render_template("get_readings.html")

    elif fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        db_conn = g.db_conn
        readings = await readings_services.get_readings(db_conn, passport)

        if readings is not False:
            return fl.render_template("successful_get_readings.html",
                                      passport=passport,
                                      electricity=readings[0],
                                      cold_water=readings[1],
                                      hot_water=readings[2],
                                      gas=readings[3])
        return fl.render_template("lose_get_readings.html")