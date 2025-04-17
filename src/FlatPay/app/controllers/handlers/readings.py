import logging

import quart as qa
from quart import g, session
from aiosqlite import Connection
from pydantic import EmailStr

from FlatPay.app.models import Readings
from FlatPay.services.payments import update_next_debt
from FlatPay.utils.validators import is_early
from FlatPay.database.repositories.readings_repo import fetch_user_readings_repo, update_user_readings_repo


# Инициализируем логирование
logger = logging.getLogger("readings_handlers")


async def update_user_readings() -> str:
    """
    Обработчик обновления показаний счётчиков.

    GET-запрос:
     - Если обновление ещё недоступно, отображает предупреждение.
     - Иначе — отображает форму для ввода показаний.

    POST-запрос:
     - Валидирует данные показаний счётчиков и обновляет задолженность пользователя.
     - Возвращает HTML-страницу с оповещением об успешном обновлении или с сообщением об ошибке.
    """

    request = qa.request
    # Получаем соединение с базой данных
    connection: Connection = g.db_conn
    # Получаем email пользователя из сессии
    email: EmailStr = session.get("user_email")

    if request.method == "GET":
        # Если обновление недоступно (по дате), показываем предупреждение
        template = "early_update_readings.html" if is_early() else "update_readings.html"
        return await qa.render_template(template)

    elif request.method == "POST":
        # Получаем данные из формы и создаем объект с показаниями
        form_data = await request.form
        readings = Readings(
            meter_readings={
                "electricity": float(form_data.get("electricity") or 0),
                "cold_water": float(form_data.get("cold_water") or 0),
                "hot_water": float(form_data.get("hot_water") or 0),
                "gas": float(form_data.get("gas") or 0)
            }
        )

        try:
            # Обновляем показания и задолженность пользователя
            await update_user_readings_repo(connection, email, readings)
            await update_next_debt(connection, email, readings)

            # Отправляем страницу с подтверждением успеха
            return await qa.render_template("successful_update_readings.html", email=email)

        except Exception as e:
            logger.error(f"Ошибка при обновлении показаний для {email}: {e}")

            # Отправляем страницу с ошибкой
            return await qa.render_template("lose_update_readings.html")


async def get_readings_info() -> str:
    """
    Обработчик получения показаний счётчиков.

    GET-запрос:
        - Извлекает email пользователя из сессии, получает показания из базы данных
          и отображает их в HTML-формате.

    Возвращаемое значение:
        - str: HTML-страница с информацией о показаниях или с сообщением об ошибке.
    """

    # Обрабатываем только GET-запрос
    request = qa.request
    # Получаем соединение с базой данных
    connection: Connection = g.db_conn
    # Получаем email пользователя из сессии
    email: EmailStr = session.get("user_email")

    if request.method == "GET":

        try:
            # Получаем показания из базы
            readings = await fetch_user_readings_repo(connection, email)

            # Делаем распаковку значений для удобства
            electricity, cold_water, hot_water, gas = readings

            # Отправляем страницу с показаниями
            return await qa.render_template(
                "user_readings.html",
                passport=email,
                electricity=electricity,
                cold_water=cold_water,
                hot_water=hot_water,
                gas=gas
            )

        except Exception as e:
            logger.error(f"Ошибка при получении показаний для {email}: {e}")

            # Возвращаем страницу с ошибкой
            return await qa.render_template("error_readings.html")
