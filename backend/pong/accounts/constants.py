import dataclasses
from typing import Final

from pong.custom_response import custom_response


@dataclasses.dataclass(frozen=True)
class UserFields:
    ID: str = "id"
    USERNAME: str = "username"
    EMAIL: str = "email"
    PASSWORD: str = "password"


@dataclasses.dataclass(frozen=True)
class PlayerFields:
    ID: str = "id"
    USER: str = "user"
    DISPLAY_NAME: str = "display_name"
    AVATAR: str = "avatar"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"


MAX_AVATAR_FILE_NAME_LENGTH: Final[int] = 50


@dataclasses.dataclass(frozen=True)
class Code:
    ALREADY_EXISTS: str = "already_exists"
    INVALID_EMAIL: str = "invalid_email"
    INVALID_PASSWORD: str = "invalid_password"
    INTERNAL_ERROR: str = custom_response.Code.INTERNAL_ERROR
