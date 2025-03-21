import flask as fl
from flask import g

from .routes import blueprint
from database.database import get_connection, close_connection


app = fl.Flask(__name__, template_folder="../templates")
app.register_blueprint(blueprint, url_prefix="/vba")


@app.before_request
async def before_request():
    """Создаем соединение для передачи хендлерам"""

    if "db_conn" not in g:
        g.db_conn = await get_connection()


@app.teardown_appcontext
def close_connection(exception=None):
    """Закрываем базу данных"""

    db_con = g.pop("db_conn", None)
    if db_con is not None:
        close_connection(db_con)
