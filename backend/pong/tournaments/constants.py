import dataclasses
from enum import Enum


@dataclasses.dataclass(frozen=True)
class TournamentFields:
    ID: str = "id"
    CREATED_AT: str = "created_at"
    STATUS: str = "status"

    class StatusEnum(Enum):
        MATCHING = "matching"
        PLAYING = "playing"
        END = "end"
