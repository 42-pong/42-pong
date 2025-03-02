from enum import Enum
from typing import Final


class BaseEnum(Enum):
    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()


class Category(BaseEnum):
    LOGIN = "LOGIN"
    STATUS = "STATUS"
    MATCH = "MATCH"
    # TODO: 他のカテゴリーは順次追加する


PAYLOAD_KEY: Final[str] = "payload"
DATA_KEY: Final[str] = "data"
