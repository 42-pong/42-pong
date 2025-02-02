import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class JWTValidator:
    def _validate_payload(self, payload: dict) -> None:
        """
        ペイロードを検証する関数

        "sub" (Subject): JWT が対象を示すクレーム。
        - 検証:
            - str型かどうか
            - 62種からなる英数字かどうか
            - 文字数が7文字かどうか

        "exp" (Expiration Time): JWT の有効期限を示すクレーム。有効期限が過ぎるとそのトークンは無効となる。
        - 検証:
            - int型かどうか
            - 現在の時刻以上であるかどうか

        "iat" (Issued At): JWT が発行された時間を示すクレーム。
        - 検証:
            - int型かどうか
            - 現在時刻以下であるかどうか

        Raises:
            ValueError:
                - sub, exp, iat以外のクレームが含まれている場合
        """
        allowed_claims = {"sub", "exp", "iat"}
        extra_claims = set(payload.keys()) - allowed_claims
        if extra_claims:
            error_message = (
                f"Unexpected claims found: {', '.join(extra_claims)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

        sub = payload.get("sub")
        if not isinstance(sub, str):
            error_message = "'sub' must be a string."
            logger.error(error_message)
            raise ValueError(error_message)
        if not re.fullmatch(r"[A-Za-z0-9]{7}", sub):
            error_message = "'sub' must be exactly 7 alphanumeric characters."
            logger.error(error_message)
            raise ValueError(error_message)

        now = int(datetime.utcnow().timestamp())
        exp = payload.get("exp")
        if not isinstance(exp, int):
            error_message = "'exp' must be an integer."
            logger.error(error_message)
            raise ValueError(error_message)
        if exp < now:
            error_message = (
                "'exp' must be greater than or equal to the current time."
            )
            logger.error(error_message)
            raise ValueError(error_message)

        iat = payload.get("iat")
        if not isinstance(iat, int):
            error_message = "'iat' must be an integer."
            logger.error(error_message)
            raise ValueError(error_message)
        if iat > now:
            error_message = (
                "'iat' must be less than or equal to the current time."
            )
            logger.error(error_message)
            raise ValueError(error_message)
