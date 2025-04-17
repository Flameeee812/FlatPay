import logging
from aiosqlite import Connection

from FlatPay.database.repositories.readings_repo import reset_meter_readings_repo


# Инициализируем логирование
logger = logging.getLogger("readings_services")


async def reset_readings(connection: Connection) -> None:
    """
    Сервис для обнуления показаний счётчиков всех пользователей.

    Параметры:
     - connection (Connection): Активное подключение к базе данных.
    """

    try:
        # Обнуляем показания счетчиков
        await reset_meter_readings_repo(connection)
        logger.info("Все показания счётчиков успешно обнулены.")

    except Exception as e:
        logger.exception(f"Ошибка при сбросе показаний счётчиков: {e}")
    