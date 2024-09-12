import os

from dotenv import load_dotenv

load_dotenv("../.env")


class Config:
    def __init__(self):
        self.POSTGRES_DB = os.environ.get("POSTGRES_DB")
        self.POSTGRES_USER = os.environ.get("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
        self.POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
        self.POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
        self.POSTGRES_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        self.SECRET_TOKEN_FOR_AUTH = os.environ.get("SECRET_TOKEN_FOR_AUTH")


config = Config()
