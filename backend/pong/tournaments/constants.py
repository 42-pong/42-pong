import dataclasses
from enum import Enum


@dataclasses.dataclass(frozen=True)
class TournamentFields:
    ID: str = "id"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
    STATUS: str = "status"

    class StatusEnum(Enum):
        MATCHING = "matching"
        PLAYING = "playing"
        END = "end"


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
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"
        CANCELED = "canceled"
