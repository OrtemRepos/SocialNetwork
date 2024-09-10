import uuid

from fastapi_users import FastAPIUsers

from auth.service.user import auth_backend, get_user_manager
from user.model import User

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_verified = fastapi_users.current_user(active=True, verified=True)
current_active_superuser = fastapi_users.current_user(
    active=True, superuser=True, verified=True
)
