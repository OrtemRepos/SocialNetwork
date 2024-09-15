from typing import Any


class InvalidID(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class UserNotExists(Exception):
    pass


class UserInactive(Exception):
    pass


class UserAlreadyVerified(Exception):
    pass


class InvalidVerifyToken(Exception):
    pass


class InvalidResetPasswordToken(Exception):
    pass


class InvalidPasswordException(Exception):
    def __init__(self, reason: Any) -> None:
        self.reason = reason
