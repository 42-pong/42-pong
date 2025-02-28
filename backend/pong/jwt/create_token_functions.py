import logging
from datetime import datetime

from . import jwt

logger = logging.getLogger(__name__)


def create_token(user_id: int, token_type: str) -> str:
    """
    指定されたuser_idとtoken_typeの応じてトークンを作成する関数

    エラーの場合は空文字を返す
    - token_typeが"access" または "refresh"以外の場合
    - jwt.encodeでエラーが発生した場合（予期せぬエラー）
    """
    jwt_handler: jwt.JWT = jwt.JWT()
    now: int = int(datetime.utcnow().timestamp())

    exp_time: dict = {"access": now + 500, "refresh": now + 3600}
    exp = exp_time.get(token_type)
    if exp is None:
        logger.error(f"Invalid token type: {token_type}")
        return ""

    token_payload: dict = {
        "sub": user_id,
        "exp": exp,
        "iat": now,
        "typ": token_type,
    }
    try:
        return jwt_handler.encode(token_payload)
    except ValueError as e:
        logger.error(f"Token encoding failed: {e}")
        return ""


def create_access_and_refresh_token(user_id: int) -> dict:
    """
    指定されたuser_idに対してアクセストークンとリフレッシュトークンを作成する関数

    この関数では `user_id` の存在確認を行わないため、事前に存在するユーザーかどうか検証する必要があります
    """
    tokens: dict = {}
    tokens["access"] = create_token(user_id, "access")
    tokens["refresh"] = create_token(user_id, "refresh")
    return tokens
