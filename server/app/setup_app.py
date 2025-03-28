import quart as qa
from quart import g, Quart, Response
from aiosqlite import Connection

from .routes import blueprint
from server.database import get_connection, close_connection


def create_app() -> Quart:
    """Фабрика для создания экземпляра приложения Quart."""

    app = qa.Quart(
        __name__,
        template_folder="../../client/templates",
        static_folder='../../client/static'
    )

    # Регистрация blueprint с префиксом
    app.register_blueprint(blueprint, url_prefix="/vba")

    # Регистрация обработчиков
    app.before_request(before_request)
    app.after_request(after_request)

    return app


async def before_request() -> None:
    """
    Функция, которая выполняется перед каждым запросом.

    - Создаёт подключение к базе данных и сохраняет его в объекте `g`,
      чтобы передать его хендлерам для дальнейшего использования.
    """

    if not hasattr(g, 'db_conn'):
        g.db_conn = await get_connection()

    return None


async def after_request(response: Response) -> Response:
    """
    Функция, которая выполняется после обработки запроса.

    - Закрывает подключение к базе данных, если оно было создано,
      освобождая ресурсы.
    """

    db_conn: Connection | None = g.pop('db_conn', None)

    if db_conn is not None:
        await close_connection(db_conn)

    return response
