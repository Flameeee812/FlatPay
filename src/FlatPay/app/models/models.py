from pydantic import BaseModel, Field


class Readings(BaseModel):
    """
    Модель для хранения показаний счетчиков
    """
    meter_readings: dict[str, int] = Field(default_factory=dict)


class NewPayment(BaseModel):
    """
    Модель для регистрации нового платежа.
    """

    amount: float

