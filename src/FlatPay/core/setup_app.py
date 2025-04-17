import quart as qa
from quart import Quart

from FlatPay.app.controllers.routes import blueprint
from FlatPay.core.middlewares import before_request, after_request


def setup_app(secret_key: str) -> Quart:
    """
    Фабрика для создания и настройки экземпляра приложения Quart.

    Параметры:
     - secret_key (str): Секретный ключ для подписи cookies и сессий.

    Возвращает:
     - app (Quart): Настроенное приложение.
    """

    app = qa.Quart(
        __name__,
        template_folder="../app/views/templates",  # Путь к HTML-шаблонам
        static_folder='../app/views/static'  # Путь к статике (CSS, изображения и т.д.)
    )

    # Устанавливаем секретный ключ для безопасности сессий
    app.secret_key = secret_key

    # Регистрируем маршруты через blueprint (группировка view-функций)
    # url_prefix добавляет ко всем маршрутам префикс /FlatPay
    app.register_blueprint(blueprint, url_prefix="/FlatPay")

    # Подключаем middleware-функции
    app.before_request(before_request)  # Выполняется до каждого запроса и открывает соединение с базой данных
    app.after_request(after_request)  # Выполняется до каждого запроса и закрывает соединение с базой данных

    # Возвращаем готовое приложение
    return app
