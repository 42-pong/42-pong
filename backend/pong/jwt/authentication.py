import logging
from typing import Optional

from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from . import exceptions, jwt

logger = logging.getLogger(__name__)


class CustomJWTAuthentication(BaseAuthentication):
    www_authenticate_realm: str = "api"

    def authenticate(self, request: Request) -> Optional[tuple]:
        auth_header = request.headers.get("Authorization")
        if auth_header is None or not auth_header.startswith("Bearer "):
            # ゲストがログインする場合もあるので、AuthenticationFailedを投げずにNoneを返す
            logger.warning(
                "Authorization header is not included or not in Bearer format"
            )
            return None

        token: str = auth_header.split(" ")[1]
        jwt_handler: jwt.JWT = jwt.JWT()
        try:
            payload: dict = jwt_handler.decode(token)
        except exceptions.TokenExpiredError as e:
            raise AuthenticationFailed(str(e), code=e.code)
        except exceptions.InvalidTokenError as e:
            logger.error(e)
            logger.error(f"Failed to decode token: {token}")
            raise AuthenticationFailed(str(e), code=e.code)
        except Exception as e:
            logger.error(e)
            raise AuthenticationFailed(str(e), code="invalid_token")

        user_id = payload.get("sub")
        if user_id is None:
            error_message = "user_id is not included in the payload"
            logger.error(error_message)
            raise AuthenticationFailed(error_message, code="invalid_token")

        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            error_message = f"User does not exist: {user_id}"
            logger.error(error_message)
            raise AuthenticationFailed(error_message, code="not_exists")
        return user, token

    # todo: viewsetに自作JWTクラスを設定後、401のステータスコードを確認するテストケース作成する
    def authenticate_header(self, request: Request) -> str:
        return f"Bearer realm={self.www_authenticate_realm}"
