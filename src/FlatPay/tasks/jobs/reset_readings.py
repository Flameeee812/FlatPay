import logging
from FlatPay.database import get_connection, close_connection
from FlatPay.services.readings import reset_readings


# Инициализируем логирование
logger = logging.getLogger("reset_readings_task")


async def schedule_reset_readings(db_path: str) -> None:
    """
    Обнуляет показания счётчиков пользователей.

    Описание:
    - Устанавливает соединение с базой данных.
    - Сбрасывает данные о показаниях счётчиков.

    Параметры:
    - db_path (str): Путь к файлу базы данных.
    """

    try:
        # Открываем асинхронное соединение с базой данных
        connection = await get_connection(path=db_path)
        # Обнуляем показания счётчиков у всех пользователей
        await reset_readings(connection)
        # Закрываем соединение с базой
        await close_connection(connection)

    except Exception as e:
        logger.warning(f"Ошибка при выполнении задачи schedule_reset_readings: {e}")
