import logging
from FlatPay.database import get_connection, close_connection
from FlatPay.services.payments import update_current_debt


# Инициализируем логирование
logger = logging.getLogger("reset_debt_task")


async def schedule_reset_debt(db_path: str) -> None:
    """
    Переносит задолженность пользователей в основной долг.

    Описание:
    - Устанавливает соединение с базой данных.
    - Обновляет текущий долг пользователей.

    Параметры:
    - db_path (str): Путь к файлу базы данных.
    """

    try:
        # Открываем асинхронное соединение с базой данных
        connection = await get_connection(path=db_path)
        # Обновляем текущую задолженность у всех пользователей
        await update_current_debt(connection)
        # Закрываем соединение с базой
        await close_connection(connection)

    except Exception as e:
        logger.warning(f"Ошибка при выполнении задачи schedule_reset_debt: {e}")