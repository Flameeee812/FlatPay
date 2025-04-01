def normalize_passport(passport: str) -> str:
    """Нормализует номер паспорта, оставляя только цифры.

    Параметры:
     - passport (str): Строка с номером паспорта (может содержать пробелы/дефисы)

    Возвращаемое значение:
     - normalized_passport (str): Нормализованный номер (только цифры)
    """

    normalized_passport = ''.join(filter(lambda char: char.isdigit(), passport))
    return normalized_passport
