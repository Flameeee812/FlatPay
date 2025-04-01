from quart import g, Response
from aiosqlite import Connection

from FlatPay.database import get_connection, close_connection
from FlatPay.core import SettingsManager


async def before_request() -> None:
    """
    Мидлварь для инициализизации соединение с БД и сохранения его в g.

    - Создаёт подключение к базе данных и сохраняет его в объекте `g`,
      чтобы передать его хендлерам для дальнейшего использования.
    """

    if not hasattr(g, 'db_conn'):
        db_path = SettingsManager.get_config().DATABASE_PATH
        db_conn = await get_connection(path=db_path)
        g.db_conn = db_conn


async def after_request(response: Response) -> Response:
    """
    Мидлварь, для закрытия соединения.

    - Закрывает подключение к базе данных, если оно было создано,
      освобождая ресурсы.
    """

    db_conn: Connection = g.pop('db_conn', None)

    if db_conn is not None:
        await close_connection(connection=db_conn)

    return response
