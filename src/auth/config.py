import os

from dotenv import load_dotenv

load_dotenv("src/auth/.auth.env")


class Config:
    def __init__(self):
        self.SECRET_TOKEN_FOR_AUTH = os.environ.get("SECRET_TOKEN_FOR_AUTH")
        self.SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
        self.SMTP_HOST = os.environ.get("SMTP_HOST")
        self.SMTP_PORT = os.environ.get("SMTP_PORT")
        self.SMTP_USER = os.environ.get("SMTP_USER")


config = Config()
