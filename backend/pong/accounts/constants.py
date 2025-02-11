import dataclasses


@dataclasses.dataclass(frozen=True)
class UserFields:
    ID: str = "id"
    USERNAME: str = "username"
    EMAIL: str = "email"
    PASSWORD: str = "password"


@dataclasses.dataclass(frozen=True)
class PlayerFields:
    USER: str = "user"
    DISPLAY_NAME: str = "display_name"
    AVATAR: str = "avatar"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
