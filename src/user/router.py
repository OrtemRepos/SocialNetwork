from fastapi import APIRouter

from src.auth.dependencies import fastapi_users
from src.auth.schema import UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
