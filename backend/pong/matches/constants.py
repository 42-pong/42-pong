import dataclasses
from enum import Enum


@dataclasses.dataclass(frozen=True)
class MatchFields:
    ID: str = "id"
    ROUND_ID: str = "round_id"
    STATUS: str = "status"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"

    class StatusEnum(Enum):
        NOT_STARTED = "not_started"
        ON_GOING = "on_going"
        COMPLETED = "completed"
        CANCELED = "canceled"


@dataclasses.dataclass(frozen=True)
class ParticipationFields:
    ID: str = "id"
    MATCH_ID: str = "match_id"
    PLAYER_ID: str = "player_id"
    TEAM: str = "team"
    CREATED_AT: str = "created_at"

    class TeamEnum(Enum):
        ONE = "1"
        TWO = "2"


@dataclasses.dataclass(frozen=True)
class ScoreFields:
    ID: str = "id"
    MATCH_PARTICIPATION_ID: str = "match_participation_id"
    CREATED_AT: str = "created_at"
    POS_X: str = "pos_x"
    POS_Y: str = "pos_y"
