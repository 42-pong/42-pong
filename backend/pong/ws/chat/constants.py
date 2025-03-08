from typing import Final

from ..share import constants as ws_constants


class Type(ws_constants.BaseEnum):
    DM = "DM"
    INVITE = "INVITE"
    GROUP_CHAT = "GROUP_CHAT"
    GROUP_ANNOUNCEMENT = "GROUP_ANNOUNCEMENT"


class GroupAnnouncement:
    PLAYER1 = "player1"
    PLAYER2 = "player2"

    class MessageType(ws_constants.BaseEnum):
        JOIN = "JOIN"
        LEAVE = "LEAVE"
        MATCH_START = "MATCH_START"


FROM: Final[str] = "from"
TO: Final[str] = "to"
CONTENT: Final[str] = "content"
TOURNAMENT_ID: Final[str] = "TOURNAMENT_ID"
MESSAGE_TYPE: Final[str] = "message_type"
