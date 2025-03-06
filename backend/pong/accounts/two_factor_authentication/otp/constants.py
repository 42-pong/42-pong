import dataclasses


@dataclasses.dataclass(frozen=True)
class OptFields:
    ID: str = "id"
    TEMP_USER: str = "temp_user"
    TEMP_USER_ID: str = "temp_user_id"
    OTP_CODE: str = "otp_code"
    CREATED_AT: str = "created_at"
