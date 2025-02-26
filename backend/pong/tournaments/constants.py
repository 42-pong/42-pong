import dataclasses
from enum import Enum
from typing import Final

MAX_PARTICIPATIONS: Final[int] = 4


@dataclasses.dataclass(frozen=True)
class TournamentFields:
    ID: str = "id"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
    STATUS: str = "status"

    class StatusEnum(Enum):
        NOT_STARTED = "not_started"
        ON_GOING = "on_going"
        COMPLETED = "completed"
        CANCELED = "canceled"


@dataclasses.dataclass(frozen=True)
class ParticipationFields:
    ID: str = "id"
    TOURNAMENT_ID: str = "tournament_id"
    PLAYER_ID: str = "player_id"
    PARTICIPATION_NAME: str = "participation_name"
    RANKING: str = "ranking"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"


@dataclasses.dataclass(frozen=True)
class RoundFields:
    ID: str = "id"
    TOURNAMENT_ID: str = "tournament_id"
    ROUND_NUMBER: str = "round_number"
    STATUS: str = "status"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"

    class StatusEnum(Enum):
        NOT_STARTED = "not_started"
        ON_GOING = "on_going"
        COMPLETED = "completed"
        CANCELED = "canceled"
