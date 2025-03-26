from typing import Final

from ..share import constants as ws_constants

USER_NAMESPACE: Final[str] = "user"
CHANNEL_RESOURCE: Final[str] = "channels"

USER_ID: Final[str] = "user_id"
ONLINE_FRIEND_IDS: Final[str] = "online_friend_ids"
ONLINE: Final[str] = "online"


class Status(ws_constants.BaseEnum):
    OK = "OK"
    ERROR = "ERROR"
