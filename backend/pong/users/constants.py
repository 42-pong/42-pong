import dataclasses
from typing import Final

from pong.custom_response import custom_response


@dataclasses.dataclass(frozen=True)
class Code:
    INVALID: Final[str] = "invalid"
    NOT_EXISTS: Final[str] = "not_exists"
    INTERNAL_ERROR: Final[str] = custom_response.Code.INTERNAL_ERROR


@dataclasses.dataclass(frozen=True)
class UsersFields:
    IS_FRIEND: Final[str] = "is_friend"
    IS_BLOCKED: Final[str] = "is_blocked"
    MATCH_WINS: Final[str] = "match_wins"
    MATCH_LOSSES: Final[str] = "match_losses"
