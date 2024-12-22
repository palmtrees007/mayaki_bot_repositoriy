from environs import Env

from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class DataBase:
    pass


@dataclass
class Config:
    tg_bot: TgBot
    data_base: DataBase


def load_config(path = None) -> Config:
    env = Env()

    env.read_env(path)

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        data_base=DataBase
    )