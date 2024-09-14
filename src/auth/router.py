from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi_users import BaseUserManager, exceptions, models, schemas
from fastapi_users.router.common import ErrorCode, ErrorModel
from pydantic import EmailStr

from src.auth.dependencies import fastapi_users
from src.auth.schema import UserCreate, UserRead, UserUpdate
from src.auth.service import auth_backend, get_user_manager

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)


@router.get(
    "/verify/{token}",
    response_model=UserUpdate,
    name="verify:verify",
    tags=["auth"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.VERIFY_USER_BAD_TOKEN: {
                            "summary": "Bad token, not existing user or"
                            "not the e-mail currently set for the user.",
                            "value": {
                                "detail": ErrorCode.VERIFY_USER_BAD_TOKEN
                            },
                        },
                        ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                            "summary": "The user is already verified.",
                            "value": {
                                "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED  # noqa: E501
                            },
                        },
                    }
                }
            },
        }
    },
)
async def verify(
    request: Request,
    token: str,
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(  # noqa: B008
        get_user_manager
    ),
):
    try:
        user = await user_manager.verify(token, request)
        return schemas.model_validate(UserRead, user)
    except (exceptions.InvalidVerifyToken, exceptions.UserNotExists) as exec:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
        ) from exec
    except exceptions.UserAlreadyVerified as exec:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
        ) from exec


@router.post(
    "/request-verify-token",
    status_code=status.HTTP_202_ACCEPTED,
    name="verify:request-token",
    tags=["auth"]
)
async def request_verify_token(
    request: Request,
    email: EmailStr = Body(..., embed=True),  # noqa: B008
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(  # noqa: B008
        get_user_manager
    ),
):
    try:
        user = await user_manager.get_by_email(email)
        await user_manager.request_verify(user, request)
    except (
        exceptions.UserNotExists,
        exceptions.UserInactive,
        exceptions.UserAlreadyVerified,
    ):
        pass

    return None
