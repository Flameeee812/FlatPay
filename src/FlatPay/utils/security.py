import os
import hashlib


def hash_password(password: str, salt: bytes = None) -> tuple[str, str] | str:
    """
    Хеширует пароль с использованием SHA-256 и соли.

    - Если соль не передана, генерируется новая соль, и возвращается кортеж (hash, salt).
    - Если соль передана, возвращается только хеш пароля.

    Параметры:
    - password (str): Пароль в открытом виде.
    - salt (bytes | None): Соль в байтах. Если не передана, будет создана новая.

    Возвращаемое значение:
    - tuple[str, str]: Хеш и соль (в hex), если соль не передана.
    - str: Только хеш, если соль передана.
    """

    # Преобразуем пароль в байты
    encoded_password = password.encode('utf-8')

    # Если не передаем соль в аргументах:
    if salt is None:
        # Создаем соль динамически
        salt = os.urandom(16)
        # "Солим" пароль
        salted_password = salt + encoded_password
        # Хэщируем пароль, спользуя sha256
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        # Возвращаем хеш и соль в hex-представлении
        return hashed_password, salt.hex()

    # Если соль передана:
    else:
        # "Солим" пароль
        salted_password = salt + encoded_password
        # Хэщируем пароль, спользуя sha256
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        # Возвращаем только хеш
        return hashed_password
