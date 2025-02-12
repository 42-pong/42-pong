import logging
from typing import Optional

from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from . import jwt

logger = logging.getLogger(__name__)


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # ゲストがログインする場合もあるので、AuthenticationFailedを投げずにNoneを返す
            logger.warning(
                "Authorization header is not included or not in Bearer format"
            )
            return None

        token: str = auth_header.split(" ")[1]
        try:
            jwt_handler: jwt.JWT = jwt.JWT()
            payload: dict = jwt_handler.decode(token)
            user_id = payload.get("sub")

            if not user_id:
                logger.error("user_id is not included in the payload")
                raise AuthenticationFailed(
                    {"status": "error", "code": "invalid_token"}
                )

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                logger.error("User does not exist")
                raise AuthenticationFailed(
                    {"status": "error", "code": "not_exist"}
                )
            return user, token

        # todo: 例外処理の詳細を記述
        # - jwt.TokenExpiredError: トークンが有効期限切れの場合
        # - jwt.InvalidTokenError: 不正なトークンの場合
        # except TokenExpiredError:
        #     raise AuthenticationFailed(
        #         # todo: "auth": "token_expired" にするかも
        #         {"status": "error", "code": "token_expired"}
        #     )

        # except jwt.InvalidTokenError:
        #     raise AuthenticationFailed(
        #         {"status": "error", "code": "invalid_token"}
        #     )
        except ValueError as e:
            logger.error(e)
            logger.error(f"Failed to decode token: {token}")
            raise AuthenticationFailed(
                {"status": "error", "code": "invalid_token"}
            )
