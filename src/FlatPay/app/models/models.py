from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    """
    Модель для пользователя с электронной почтой и паролем.

    Параметры:
     - email (EmailStr): Электронная почта пользователя.
     - password (str): Пароль пользователя, минимальная длина — 8 символов.
    """
    email: EmailStr
    password: str = Field(min_length=8)


class Readings(BaseModel):
    """
    Модель для хранения показаний счетчиков.

    Содержит словарь с типами счетчиков в качестве ключей и их показаниями в качестве значений.

    Параметры:
     - meter_readings (dict[str, int]): Словарь с показаниями счетчиков, где ключ — тип счетчика
                                        (например, 'electricity'), а значение — соответствующее показание.
    """

    meter_readings: dict[str, int] = Field(default_factory=dict)


class Payment(BaseModel):
    """
    Модель для регистрации нового платежа.

    Параметры:
     - amount (float): Сумма платежа.
    """

    amount: float

