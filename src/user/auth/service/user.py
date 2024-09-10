import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from user.config import config
from user.database import get_user_db
from user.user.model import User

SECRET = config.SECRET_TOKEN_FOR_AUTH


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):  # noqa: E501
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"""User {user.id} hasforgot their
              password.Reset token: {token}"""
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"""Verification requested for user {user.id}.
              Verification token: {token}"""
        )


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):  # noqa: E501
    yield UserManager(user_db)


cookie_transport = CookieTransport(
    cookie_max_age=3600, cookie_name="fastapi_users"
)  # noqa: E501


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
