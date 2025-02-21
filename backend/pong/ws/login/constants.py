from typing import Final

from ..share import constants as ws_constants

USER_NAMESPACE: Final[str] = "user"
CHANNEL_RESOURCE: Final[str] = "channels"

USER_ID: Final[str] = "user_id"


class Status(ws_constants.BaseEnum):
    OK = "OK"
    ERROR = "ERROR"
