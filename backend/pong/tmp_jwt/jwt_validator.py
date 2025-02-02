import logging

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
            error_message: str = (
                f"Unexpected claims found: {', '.join(extra_claims)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)
        """
