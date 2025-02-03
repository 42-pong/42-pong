import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class JWTValidator:
    # todo: validate_jwt作成
    # - ヘッダー、ペイロード、シグネチャがデコードできるかどうかを検証する
    # todo: _validate_header作成
    # - {"typ": "JWT", "alg": "HS256"} であることを検証する
    def _validate_payload(self, payload: dict) -> None:
        """
        ペイロードを検証する関数

        "sub" (Subject): JWT が対象を示すクレーム。今回はユーザーIDを示す
        - str型
        - 62種からなる英数字
        - 文字数が7文字

        "exp" (Expiration Time): JWT の有効期限を示すクレーム。有効期限が過ぎるとそのトークンは無効となる。
        - int型
        - 現在の時刻以上である

        "iat" (Issued At): JWT が発行された時間を示すクレーム。
        - int型
        - 現在時刻以下である

        "typ" (Type): JWTの種類を示すクレーム。今回はアクセストークンとリフレッシュトークンの2種類を扱う。
        - str型
            - "access"（アクセストークン）
            - "refresh"（リフレッシュトークン）

        Raises:
            ValueError:
            - sub, exp, iat以外のクレームが含まれている場合
            - subがstr型でない場合
            - subの長さが7文字未満の場合
            - subの長さが8文字以上の場合
            - subが英数字以外の文字を含む場合
            - expが整数でない場合
            - expが現在時刻より小さい場合
            - iatが整数でない場合
            - iatが現在時刻より未来の場合
        """
        allowed_claims = {"sub", "exp", "iat", "typ"}
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

        typ = payload.get("typ")
        if typ not in {"access", "refresh"}:
            error_message = "'typ' must be either 'access' or 'refresh'."
            logger.error(error_message)
            raise ValueError(error_message)
