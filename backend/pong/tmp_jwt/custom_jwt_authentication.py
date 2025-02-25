import logging
from typing import Optional

from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from . import jwt

logger = logging.getLogger(__name__)


class CustomJWTAuthentication(BaseAuthentication):
    www_authenticate_realm: str = "api"

    def authenticate(self, request: Request) -> Optional[tuple]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # ゲストがログインする場合もあるので、AuthenticationFailedを投げずにNoneを返す
            logger.warning(
                "Authorization header is not included or not in Bearer format"
            )
            return None

        token: str = auth_header.split(" ")[1]
        jwt_handler: jwt.JWT = jwt.JWT()
        payload: dict = {}
        try:
            payload = jwt_handler.decode(token)
        # todo: 例外処理の詳細を記述
        # - jwt.TokenExpiredError: トークンが有効期限切れの場合
        # - jwt.InvalidTokenError: 不正なトークンの場合
        # except TokenExpiredError:
        #     raise AuthenticationFailed(
        #         {"status": "error", "code": "token_expired"}
        #     )
        # except jwt.InvalidTokenError:
        #     logger.error(e)
        #     logger.error(f"Failed to decode token: {token}")
        #     raise AuthenticationFailed(
        #         {"status": "error", "code": "invalid_token"}
        #     )
        except Exception as e:
            logger.error(e)
            raise AuthenticationFailed(str(e), code="invalid_token")

        user_id = payload.get("sub")
        if not user_id:
            error_message = "user_id is not included in the payload"
            logger.error(error_message)
            raise AuthenticationFailed(error_message, code="invalid_token")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            error_message = f"User does not exist: {user_id}"
            logger.error(error_message)
            raise AuthenticationFailed(error_message, code="not_exists")
        return user, token

    # todo: viewsetに自作JWTクラスを設定後、401のステータスコードを確認するテストケース作成する
    def authenticate_header(self, request: Request) -> str:
        return '{} realm="{}"'.format(
            "Bearer",
            self.www_authenticate_realm,
        )
