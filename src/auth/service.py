import uuid

import redis
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    RedisStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.auth.config import config as auth_config
from src.config import config
from src.database import get_user_db
from src.email_celery.router import send_verification_email_task
from src.models import User

SECRET = auth_config.SECRET_TOKEN_FOR_AUTH
redis_connection = redis.asyncio.from_url(
    config.REDIS_URL, decode_responses=True
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: User, request: Request | None = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        print(
            f"""User {user.id} hasforgot their
              password.Reset token: {token}"""
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        print(
            f"""Verification requested for user {user.id}.
              Verification token: {token}"""
        )
        send_verification_email_task.delay(user.email, token)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),  # noqa: B008
):
    yield UserManager(user_db)


cookie_transport = CookieTransport(
    cookie_max_age=3600, cookie_name="fastapi_users"
)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis_connection, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt", transport=cookie_transport, get_strategy=get_redis_strategy
)
