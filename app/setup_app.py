import flask as fl
from flask import g

from .routes import blueprint
from server.database import get_connection, close_connection


# Создаём экземпляр приложения Flask
app = fl.Flask(__name__, template_folder="../client/templates", static_folder='../client/static')
# Регистрируем blueprint с префиксом "/vba" для всех URL
app.register_blueprint(blueprint, url_prefix="/vba")


@app.before_request
async def before_request() -> None:
    """
    Функция, которая выполняется перед каждым запросом.

    - Создаёт подключение к базе данных и сохраняет его в объекте `g`,
      чтобы передать его хендлерам для дальнейшего использования.
    """

    if "db_conn" not in g:
        g.db_conn = await get_connection()

    return None


@app.teardown_appcontext
def close_connection(exception=None) -> None:
    """
    Функция, которая выполняется после обработки запроса.

    - Закрывает подключение к базе данных, если оно было создано,
      освобождая ресурсы.
    """

    db_con = g.pop("db_conn", None)
    if db_con is not None:
        close_connection(db_con)

    return None
