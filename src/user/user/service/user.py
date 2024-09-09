import contextlib
import uuid
from fastapi_users import FastAPIUsers
from fastapi_users.exceptions import UserAlreadyExists
from user.auth.service.user import get_user_manager, auth_backend
from user.database import get_async_session, get_user_db

from user.user.model import User
from user.user.schema import UserCreate


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_verified = fastapi_users.current_user(active=True, verified=True)
current_active_superuser = fastapi_users.current_user(
    active=True, superuser=True, verified=True
)


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str,
    password: str,
    is_superuser: bool = False,
    is_active: bool = True,
    is_verified: bool = False,
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            first_name="admin",
                            last_name="admin",
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            is_active=is_active,
                            is_verified=is_verified,
                        )
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")
