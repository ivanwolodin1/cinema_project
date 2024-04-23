from http import HTTPStatus

from core.constants import (
    ACCESS_EXPIRATION_ERROR,
    AUTHENTICATION_ERROR,
    EXISTING_USER_ERROR,
    FORBIDDEN_FOR_ROLE_ERROR,
    NO_SUCH_ROLE_ERROR,
    NO_SUCH_USER_ERROR,
    NON_EXISTING_ROLE_ERROR,
    TOKEN_ERROR,
)


class DuplicateUserError(Exception):
    def __init__(self):
        super().__init__(EXISTING_USER_ERROR)


class InvalidRoleError(Exception):
    def __init__(self):
        super().__init__(NON_EXISTING_ROLE_ERROR)


class UserAuthenticationError(Exception):
    def __init__(self):
        super().__init__(AUTHENTICATION_ERROR)


class InvalidTokenError(Exception):
    def __init__(self):
        super().__init__(TOKEN_ERROR)


class AccessTokenExpired(Exception):
    def __init__(self):
        super().__init__(ACCESS_EXPIRATION_ERROR)


class WrongRoleId(Exception):
    def __init__(self):
        super().__init__(FORBIDDEN_FOR_ROLE_ERROR)


class RoleNotFound(Exception):
    def __init__(self):
        super().__init__(NO_SUCH_ROLE_ERROR)


class UserNotFound(Exception):
    def __init__(self):
        super().__init__(NO_SUCH_USER_ERROR)


class RoleAlreadyExist(Exception):
    def __init__(self):
        super().__init__(NO_SUCH_USER_ERROR)


exception_mappings = {
    DuplicateUserError: HTTPStatus.CONFLICT,
    InvalidRoleError: HTTPStatus.BAD_REQUEST,
    UserAuthenticationError: HTTPStatus.UNAUTHORIZED,
    InvalidTokenError: HTTPStatus.UNAUTHORIZED,
    WrongRoleId: HTTPStatus.FORBIDDEN,
    RoleNotFound: HTTPStatus.NOT_IMPLEMENTED,
    UserNotFound: HTTPStatus.BAD_REQUEST,
    RoleAlreadyExist: HTTPStatus.CONFLICT,
}
