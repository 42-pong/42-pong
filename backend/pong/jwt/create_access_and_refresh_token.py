import logging
from datetime import datetime

from jwt import jwt

logger = logging.getLogger(__name__)


# todo: リファクタリング
# - typによってexpの時間を変える関数作成
def create_access_and_refresh_token(user_id: int) -> dict:
    jwt_handler: jwt.JWT = jwt.JWT()
    now: int = int(datetime.utcnow().timestamp())
    # アクセストークンの有効期限は10分にしています
    access_payload: dict = {
        "sub": user_id,
        "exp": now + 500,
        "iat": now,
        "typ": "access",
    }
    # リフレッシュトークンの有効期限は1時間にしています
    refresh_payload: dict = {
        "sub": user_id,
        "exp": now + 3600,
        "iat": now,
        "typ": "refresh",
    }
    tokens: dict = {}
    try:
        tokens["access"] = jwt_handler.encode(access_payload)
        tokens["refresh"] = jwt_handler.encode(refresh_payload)
    except ValueError as e:
        # 本来起こらないエラー
        logger.error(e)
    return tokens
