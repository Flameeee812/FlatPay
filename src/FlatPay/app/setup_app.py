import quart as qa
from quart import Quart

from FlatPay.app.controllers.routes import blueprint
from .middlewares import before_request, after_request


def setup_app() -> Quart:
    """Фабрика для создания экземпляра приложения Quart."""

    app = qa.Quart(
        __name__,
        template_folder="../../templates",
        static_folder='../../static'
    )

    # Регистрация blueprint с префиксом
    app.register_blueprint(blueprint, url_prefix="/FlatPay")

    # Регистрация мидлварей
    app.before_request(before_request)
    app.after_request(after_request)

    return app
