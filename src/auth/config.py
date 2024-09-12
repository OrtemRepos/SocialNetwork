import os

from dotenv import load_dotenv

load_dotenv(".env")

SECRET_TOKEN_FOR_AUTH = os.environ.get("SECRET_TOKEN_FOR_AUTH")
