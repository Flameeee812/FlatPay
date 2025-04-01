from FlatPay.app.models.models import Readings


def calculate_base_debt(readings: Readings) -> float:
    """
    Утилита для подсчёта долга по актуальному Казансому тарифу.

    Параметры:
     - readings (dict): Словарь с показаниями для различных ресурсов (электричество, вода, газ).

    Возвращаемое значение:
     - float: Рассчитанный долг по актуальному тарифу.
    """

    tariffs = {
        "electricity": 5.09,
        "cold_water": 29.41,
        "hot_water": 226.7,
        "gas": 7.47}
    base_debt = 0.0

    for key, rate in tariffs.items():
        base_debt += readings.meter_readings[key] * rate

    return round(base_debt, 2)
