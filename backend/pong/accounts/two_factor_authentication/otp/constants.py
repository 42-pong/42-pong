import dataclasses
from typing import Final

from pong.custom_response import custom_response


@dataclasses.dataclass(frozen=True)
class OptFields:
    ID: str = "id"
    TEMP_USER: str = "temp_user"
    TEMP_USER_ID: str = "temp_user_id"
    OTP_CODE: str = "otp_code"
    CREATED_AT: str = "created_at"


OPT_CODE_LENGTH: Final[int] = 6
EXPIRED_MINUTES: Final[int] = 5


@dataclasses.dataclass(frozen=True)
class Code:
    INVALID: Final[str] = "invalid"
    INTERNAL_ERROR: Final[str] = custom_response.Code.INTERNAL_ERROR
