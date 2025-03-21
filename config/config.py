from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    DATABASE_PATH: str
    LOG_PATH: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env()

    config = Config(
        DATABASE_PATH=env("DATABASE_PATH"),
        LOG_PATH=env("LOG_PATH")
    )

    return config
