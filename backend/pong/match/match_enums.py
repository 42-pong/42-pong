from enum import Enum
from typing import Final


class Stage(Enum):
    INIT: Final[str] = "INIT"
    READY: Final[str] = "READY"
    PLAY: Final[str] = "PLAY"
    END: Final[str] = "END"
    NONE: Final[str] = "NONE"

    @classmethod
    def key(cls) -> str:
        return "stage"


class Mode(Enum):
    LOCAL: Final[str] = "local"
    REMOTE: Final[str] = "remote"

    @classmethod
    def key(cls) -> str:
        return "mode"


class Team(Enum):
    One: Final[str] = "1"
    Two: Final[str] = "2"
    Empty: Final[str] = ""

    @classmethod
    def key(cls) -> str:
        return "team"


class Move(Enum):
    UP: Final[str] = "UP"
    DOWN: Final[str] = "DOWN"

    @classmethod
    def key(cls) -> str:
        return "move"
