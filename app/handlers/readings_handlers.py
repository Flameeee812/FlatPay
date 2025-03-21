import flask as fl
from flask import g

from database.db_services import readings_services
from database.db_services.payment_services import update_debt


async def update_user_readings():
    """Хендлер для страницы обновления показаний счётчиков"""

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

        if await readings_services.update_readings(db_conn, passport, readings):
            await update_debt(db_conn, passport)
            return fl.render_template("successful_update_readings.html", passport=passport)

        return fl.render_template("lose_update_readings.html")


async def get_readings_info():
    """Хендлер для страницы получения информации о показаниях счётчиков"""

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
