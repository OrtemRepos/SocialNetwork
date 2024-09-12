from typing import Any


class InvalidID:
    pass


class UserAlreadyExists:
    pass


class UserNotExists:
    pass


class UserInactive:
    pass


class UserAlreadyVerified:
    pass


class InvalidVerifyToken:
    pass


class InvalidResetPasswordToken:
    pass


class InvalidPasswordException:
    def __init__(self, reason: Any) -> None:
        self.reason = reason
