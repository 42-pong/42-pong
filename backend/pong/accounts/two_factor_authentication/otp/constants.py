import dataclasses
from typing import Final


@dataclasses.dataclass(frozen=True)
class OptFields:
    ID: str = "id"
    TEMP_USER: str = "temp_user"
    TEMP_USER_ID: str = "temp_user_id"
    OTP_CODE: str = "otp_code"
    CREATED_AT: str = "created_at"


OPT_CODE_LENGTH: Final[int] = 6
EXPIRED_MINUTES: Final[int] = 5
