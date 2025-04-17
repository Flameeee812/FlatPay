from quart import g, Response
from aiosqlite import Connection

from FlatPay.database import get_connection, close_connection
from FlatPay.core import SettingsManager


async def before_request() -> None:
    """
    Мидлварь для инициализации соединения с БД и сохранения его в g.

    - Вызывается перед каждым запросом.
    - Проверяет, есть ли уже соединение с БД в объекте `g`.
    - Если нет — создаёт новое асинхронное соединение и сохраняет его в `g.db_conn`.
    - Это позволяет всем маршрутам в рамках одного запроса использовать общее подключение.
    """

    # Проверяем, есть ли уже подключение в контексте `g`
    if not hasattr(g, 'db_conn'):
        # Получаем путь к базе из конфигурации
        db_path = SettingsManager.get_config().DATABASE_PATH

        # Открываем соединение с базой
        db_conn = await get_connection(path=db_path)

        # Сохраняем соединение в контексте текущего запроса
        g.db_conn = db_conn


async def after_request(response: Response) -> Response:
    """
    Мидлварь для закрытия соединения с базой данных.

    - Вызывается после обработки запроса, но до отправки ответа клиенту.
    - Извлекает соединение из объекта `g` (если оно было создано).
    - Закрывает соединение, освобождая ресурсы.

    Возвращаемое значение:
     - response (Response): Ответ клиенту.
    """

    # Извлекаем подключение к БД из `g`, если оно есть (и сразу удаляем)
    db_conn: Connection = g.pop('db_conn', None)

    # Если соединение было создано — закрываем его
    if db_conn is not None:
        await close_connection(connection=db_conn)

    # Возвращаем HTTP-ответ дальше по цепочке
    return response
