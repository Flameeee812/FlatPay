import quart as qa
from quart import g, session, url_for, Response
from aiosqlite import Connection
from pydantic import ValidationError

from FlatPay.services.user import register_user
from FlatPay.utils.validators import is_correct_password, is_authenticated
from FlatPay.app.models import User


async def index_handler() -> str:
    """
    Обработчик главной страницы.

    Отображает приветственную страницу приложения.

    Возвращаемое значение:
     - str: приветственная страница.
    """

    return await qa.render_template("index.html")


async def register_handler() -> Response | str:
    """
    Обработчик регистрации пользователя.

    GET-запрос:
     - Отображает форму регистрации.
    POST-запрос:
     - Валидирует введённые данные, регистрирует пользователя и сохраняет сессию.
     - В случае успеха авторизует и сохраняет сессию.

    Возвращаемое значение:
     - Response | str: Редирект на домашнюю страницу при успехе;
                       страница ошибки регистрации при неудаче.
    """

    request = qa.request
    # Получаем соединение с базой данных
    connection: Connection = g.db_conn

    if request.method == "GET":
        # Показываем форму регистрации
        return await qa.render_template("register.html")

    elif request.method == "POST":
        # Получаем данные из формы
        form_data: dict = await request.form  # Получение данных формы
        try:
            # Создание и валидация пользователя
            user: User = User(email=form_data.get("email"), password=form_data.get("password"))
        except ValidationError:
            # Если данные некорректны — отображаем страницу ошибки
            return await qa.render_template("lose_register.html")

        # Пытаемся зарегистрировать пользователя
        if await register_user(connection, user.email, user.password):
            # Устанавливаем сессионные значения
            session["user_email"] = user.email
            session["logged_in"] = True

            # Перенаправляем пользователя в его кабинет
            return qa.redirect(url_for("blueprint.homepage"))

        # Если пользователь уже зарегистрирован или другая ошибка
        return await qa.render_template("lose_register.html")


async def login_handler() -> Response | str:
    """
    Обработчик авторизации пользователя.

    GET-запрос:
     - Отображает форму авторизации.
    POST-запрос:
     - Проверяет введённые данные, валидирует форму, проверяет логин и при успехе создаёт сессию.

    Возвращаемое значение:
     - Response | str: HTML-страница входа при неудаче, или редирект на домашнюю страницу при успехе.
    """

    request = qa.request
    # Получаем соединение с базой данных
    connection: Connection = g.db_conn
    # Получаем email пользователя из сессии

    # Обработка GET-запроса: отображение формы входа
    if request.method == "GET":
        return await qa.render_template("login.html")

    # Обработка POST-запроса: получение данных формы
    elif request.method == "POST":
        # Получаем данные формы
        form_data: dict = await request.form  # Получение данных формы
        try:
            # Создание и валидация пользователя
            user: User = User(email=form_data.get("email"), password=form_data.get("password"))
        except ValidationError:
            # Ошибка валидации формы (например, пустой email или короткий пароль)
            return await qa.render_template("lose_login.html")

        try:
            # Проверяем, корректен ли пароль (с учётом соли)
            if await is_correct_password(connection, user.email, user.password):
                # Устанавливаем сессию при успешной авторизации
                session["user_email"] = user.email
                session["logged_in"] = True

                # Перенаправляем пользователя в его кабинет
                return qa.redirect(url_for("blueprint.homepage"))

            else:
                # Если пароль не совпал
                return await qa.render_template("lose_login.html")

        except TypeError:
            # Если пользователь не зарегистрирован, то salt = None — is_correct_password вызывает TypeError
            return await qa.render_template("lose_login.html")


def dashboard_handler() -> Response | None:
    """
    Обработчик маршрута личного кабинета.

    Проверяет, авторизован ли пользователь. Если нет — перенаправляет
    на страницу входа. Если да — перенаправляет на домашнюю страницу.

    Возвращаемое значение:
     - Response: Редирект на домашнюю страницу или на страницу входа.
    """

    # Обрабатываем только GET-запрос
    request = qa.request

    if request.method == "GET":
        if not session.get("logged_in"):
            return qa.redirect(url_for("blueprint.login"))  # Перенаправляют на страницу авторизации

        return qa.redirect(url_for("blueprint.homepage"))  # Перенаправляют на домашнюю страницу


async def homepage_handler() -> Response | str:
    """
    Обработчик домашней страницы пользователя.

    Проверяет, авторизован ли пользователь, и отображает домашнюю
    страницу с адресом его электронной почты, только при активной сессии.
    В противном случае перенаправляет на страницу входа.

    Возвращаемое значение:
     - Response | str: HTML-страница homepage.html или редирект на страницу входа.
    """

    if is_authenticated():
        return await qa.render_template("homepage.html", email=session.get("user_email"))

    return qa.redirect(url_for("blueprint.login"))  # Перенаправляют на страницу авторизации


async def logout_handler() -> Response | str:
    """
    Обработчик выхода пользователя из системы.

    GET-запрос:
     - Отображает страницу подтверждения выхода.
    POST-запрос:
     - Очищает сессию пользователя и перенаправляет на главную страницу.

    Возвращаемое значение:
     - Response | str: HTML-страница подтверждения выхода или редирект.
    """

    request = qa.request

    if request.method == "GET":
        return await qa.render_template("logout_user.html")  # Показывает подтверждение выхода

    elif request.method == "POST":
        session.clear()  # Завершает сессию
        return qa.redirect(url_for("blueprint.index"))   # Перенаправляет на главную
