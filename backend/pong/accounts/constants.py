from dataclasses import dataclass


@dataclass(frozen=True)
class UserFields:
    ID: str = "id"
    USERNAME: str = "username"
    EMAIL: str = "email"
    PASSWORD: str = "password"


@dataclass(frozen=True)
class PlayerFields:
    USER: str = "user"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
