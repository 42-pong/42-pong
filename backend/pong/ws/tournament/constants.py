from typing import Final

from ..share import constants as ws_constants


class Type(ws_constants.BaseEnum):
    JOIN = "JOIN"
    LEAVE = "LEAVE"
    RELOAD = "RELOAD"
    ASSIGNED = "ASSIGNED"


class JoinType(ws_constants.BaseEnum):
    CREATE = "CREATE"
    RANDOM = "RANDOM"
    SELECTED = "SELECTED"


class Status(ws_constants.BaseEnum):
    OK = "OK"
    ERROR = "ERROR"


class Event(ws_constants.BaseEnum):
    PLAYER_CHANGE = "PLAYER_CHANGE"
    TOURNAMENT_STATE_CHANGE = "TOURNAMENT_STATE_CHANGE"


TOURNAMENT_ID: Final[str] = "tournament_id"
PARTICIPATION_NAME: Final[str] = "participation_name"
MATCH_ID: Final[str] = "match_id"
