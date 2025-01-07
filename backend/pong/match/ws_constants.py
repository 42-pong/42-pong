from enum import Enum
from typing import Final


class Category(Enum):
    MATCH: Final[str] = "MATCH"
    # TODO: 他のカテゴリーは順次追加する

    @classmethod
    def key(cls) -> str:
        return "category"


PAYLOAD_KEY: Final[str] = "payload"
DATA_KEY: Final[str] = "data"
