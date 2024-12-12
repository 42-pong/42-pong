from dataclasses import dataclass

# todo: はPlayerかUserどちらかだけで良さそう


@dataclass(frozen=True)
class UserFields:
    ID: str = "id"
    USERNAME: str = "username"
    EMAIL: str = "email"
    PASSWORD: str = "password"


@dataclass(frozen=True)
class PlayerFields:
    ID: str = "id"
    USER: str = "user"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
