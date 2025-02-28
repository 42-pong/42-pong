import logging
from datetime import datetime

from . import jwt

logger = logging.getLogger(__name__)


def create_token(user_id: int, token_type: str) -> str:
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


# todo: user_idを検証する
def create_access_and_refresh_token(user_id: int) -> dict:
    tokens: dict = {}
    tokens["access"] = create_token(user_id, "access")
    tokens["refresh"] = create_token(user_id, "refresh")
    return tokens
