class UserAlreadyExists(Exception):
    def __init__(self, reason: str):
        self.reason = reason


class InvalidPasswordException(Exception):
    def __init__(self, reason: str):
        self.reason = reason


class UserNotFoundException(Exception):
    def __init__(self, reason: str):
        self.reason = reason
