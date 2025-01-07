from enum import Enum
from typing import Final


class BaseEnum(Enum):
    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()


class Stage(BaseEnum):
    INIT: Final[str] = "INIT"
    READY: Final[str] = "READY"
    PLAY: Final[str] = "PLAY"
    END: Final[str] = "END"


class Mode(BaseEnum):
    LOCAL: Final[str] = "local"
    REMOTE: Final[str] = "remote"


class Team(BaseEnum):
    ONE: Final[str] = "1"
    TWO: Final[str] = "2"
    EMPTY: Final[str] = ""


class Move(BaseEnum):
    UP: Final[str] = "UP"
    DOWN: Final[str] = "DOWN"
