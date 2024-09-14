import os

from dotenv import load_dotenv

load_dotenv("src/auth/.auth.env")


class Config:
    def __init__(self):
        self.SECRET_TOKEN_FOR_AUTH = os.environ.get("SECRET_TOKEN_FOR_AUTH")


config = Config()
