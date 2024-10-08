import os

from dotenv import load_dotenv

load_dotenv("./.env")


class Config:
    def __init__(self):
        self.POSTGRES_DB = os.environ.get("POSTGRES_DB")
        self.POSTGRES_USER = os.environ.get("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
        self.POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
        self.POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
        self.POSTGRES_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

        self.REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
        self.REDIS_USER = os.environ.get("REDIS_USER")
        self.REDIS_PORT = os.environ.get("REDIS_PORT")
        self.REDIS_HOST = os.environ.get("REDIS_HOST")
        self.REDIS_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

        self.RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
        self.RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")
        self.RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
        self.RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
        self.RABBITMQ_HOSTNAME = os.environ.get("RABBITMQ_HOSTNAME")
        self.RABBITMQ_URL = f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_HOSTNAME}"


config = Config()
