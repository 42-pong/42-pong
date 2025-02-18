from typing import Final

from ..share import constants as ws_constants

USER_ID: Final[str] = "user_id"


class Status(ws_constants.BaseEnum):
    OK = "OK"
    ERROR = "ERROR"
