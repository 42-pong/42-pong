# views.py
import logging
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from django.urls import reverse
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from jwt.views import token
from pong import settings

from . import create_oauth2_account, models
from .providers import forty_two_authorization

logger = logging.getLogger(__name__)


class OAuth2BaseView(APIView):
    """
    OAuth2関連の共通の変数を定義する基底クラス
    """

    authentication_classes = []
    permission_classes = (AllowAny,)

    @property
    def redirect_uri(self) -> str:
        return settings.PONG_ORIGIN + reverse("oauth2:callback")


class OAuth2AuthorizeView(OAuth2BaseView):
    @extend_schema(
        request=None,
        responses={
            302: OpenApiResponse(
                description="Redirect to OAuth2 authorization URL",
                response=[
                    ("Location", str),
                ],
                examples=[
                    OpenApiExample(
                        "Example 302 Redirect",
                        value={
                            "Location": "https://example.com/oauth2/authorize?code=abc123..."
                        },
                    ),
                ],
            ),
        },
    )
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        認可エンドポイントを呼ぶ関数
        この関数はクライアント(42pong)が認可サーバーの認可エンドポイントにアクセスし、認可コードを取得するために使用する。

        認可エンドポイントを呼ぶケース
        - ユーザーが新規アカウントを作成した時
        - ユーザーが明示的にログアウトした時(ログアウト時にアクセストークンを削除する場合)
        - リフレッシュトークンの有効期限が切れた時
        """
        query_params: dict[str, str] = {
            "client_id": settings.OAUTH2_CLIENT_ID,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
        }
        query_string: str = urlencode(query_params)

        authorization_url: str = (
            f"{settings.OAUTH2_AUTHORIZATION_ENDPOINT}?{query_string}"
        )

        return Response(
            status=status.HTTP_302_FOUND,
            headers={"Location": authorization_url},
        )


class OAuth2CallbackView(OAuth2BaseView):
    @extend_schema(
        responses={
            200: OpenApiResponse(
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": {
                                "access": "eyJhbGciOiJIUzI1...",
                                "refresh": "eyJhbGciOiJIUzI1...",
                            },
                        },
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Error when no code is provided",
                examples=[
                    OpenApiExample(
                        "Example 400 Response",
                        value={
                            "error": "Authorization code is None. Please check your authentication process."
                        },
                    )
                ],
            ),
            401: OpenApiResponse(
                description="ユーザーが認証を拒否した場合、また失敗した場合",
                examples=[
                    OpenApiExample(
                        "Example 401 response",
                        value={
                            "status": "error",
                            "code": "fail",
                            "errors": {
                                "detail": "The provided authorization grant is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client."
                            },
                        },
                    ),
                ],
            ),
            500: OpenApiResponse(
                description="予期せぬエラーが発生した場合（例えば、テーブル作成に失敗したなど）",
                examples=[
                    OpenApiExample(
                        "Example 500 response",
                        value={
                            "status": "error",
                            "code": "internal_error",
                            "errors": {"detail": "Internal server error"},
                        },
                    ),
                ],
            ),
        }
    )
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        認可サーバーからのレスポンスを受け取る関数
        この関数は認可エンドポイント(`/api/oauth2/authorize`)のレスポンスを受け取り、認可コードを取得するために使用する。
        そのため、このエンドポイントはFEから呼ばれることはありません。
        """
        redirect_uri: str = f"{settings.PONG_ORIGIN}/oauth2/"

        code = request.GET.get("code")
        if code is None:
            error_query_string = "error=fail"
            error_message = "Authorization code is None. Please check your authentication process."
            logger.error(f"401 AuthenticationFailedError: {error_message}")
            return Response(
                status=status.HTTP_302_FOUND,
                headers={"Location": redirect_uri + "?" + error_query_string},
            )

        # ===== todo: def authenticate_user(code: str) -> dict:作成 ======
        # 成功: user_infoを返す
        # 失敗: 例外 AuthenticationFailedError, InternalServerError
        request_data: dict[str, str] = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "client_id": settings.OAUTH2_CLIENT_ID,
            "client_secret": settings.OAUTH2_CLIENT_SECRET_KEY,
        }

        token_response: requests.models.Response = requests.post(
            settings.OAUTH2_TOKEN_ENDPOINT,
            data=request_data,
        )
        tokens = token_response.json()
        if token_response.status_code != status.HTTP_200_OK:
            error_query_string = "error=fail"
            logger.error(
                f"401 AuthenticationFailedError: {tokens["error_description"]}"
            )
            return Response(
                status=status.HTTP_302_FOUND,
                headers={"Location": redirect_uri + "?" + error_query_string},
            )
        user_response = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {tokens["access_token"]}"},
        )
        user_info = user_response.json()
        if token_response.status_code != status.HTTP_200_OK:
            logger.error(
                f"401 AuthenticationFailedError: {user_info["error_description"]}"
            )
            error_query_string = "error=fail"
            return Response(
                status=status.HTTP_302_FOUND,
                headers={"Location": redirect_uri + "?" + error_query_string},
            )
        # =============================================================

        password_42: str = "42" + user_info["login"]
        if not models.User.objects.filter(email=user_info["email"]).exists():
            # ====== todo: OAuth2の登録（リファクタリング）======
            # 成功: oauth2_userを返す
            # 失敗: 例外, InternalServerError
            oauth2_user_result: create_oauth2_account.CreateOAuth2UserResult = create_oauth2_account.create_oauth2_user(
                user_info["email"], password_42, user_info["login"]
            )
            # todo: internal_errorのエラーハンドリングを追加する
            if not oauth2_user_result.is_ok:
                error_query_string = "error=internal_error"
                logger.error(
                    f"500 InternalServerError: {oauth2_user_result.unwrap_error()}"
                )
                return Response(
                    status=status.HTTP_302_FOUND,
                    headers={
                        "Location": redirect_uri + "?" + error_query_string
                    },
                )

            user_info = oauth2_user_result.unwrap()
            forty_two_token_data = {
                "access_token": tokens.get("access_token"),
                "token_type": tokens.get("token_type"),
                "access_token_expiry": datetime.now()
                + timedelta(seconds=tokens.get("expires_in")),
                "refresh_token": tokens.get("refresh_token"),
                "refresh_token_expiry": datetime.fromtimestamp(
                    tokens.get("secret_valid_until")
                ),
                "scope": tokens.get("scope"),
            }
            oauth2_result: forty_two_authorization.CreateFortyTwoAuthorizationResult = forty_two_authorization.create_forty_two_authorization(
                user_info["id"], "42", user_info["id"], forty_two_token_data
            )
            # 42認証のテーブルが失敗した場合は、Userテーブルを削除する
            if not oauth2_result.is_ok:
                models.User.objects.get(id=user_info["id"]).delete()
                error_query_string = "error=internal_error"
                logger.error(
                    f"500 InternalServerError: {oauth2_user_result.unwrap_error()}"
                )
                return Response(
                    status=status.HTTP_302_FOUND,
                    headers={
                        "Location": redirect_uri + "?" + error_query_string
                    },
                )
            # ==================================================================

        oauth2_user = models.User.objects.get(email=user_info["email"])
        factory = APIRequestFactory()
        request = factory.post(
            reverse("jwt:token_obtain_pair"),
            {
                "email": oauth2_user.email,
                "password": password_42,
            },
            format="json",
        )
        response = token.TokenObtainView.as_view()(request)
        if response.status_code != status.HTTP_200_OK:
            oauth2_user.delete()
            error_query_string = "error=fail"
            logger.error(
                f"{response.status_code} TokenObtainFailedError: {response.data}"
            )
            return Response(
                status=status.HTTP_302_FOUND,
                headers={"Location": redirect_uri + "?" + error_query_string},
            )
        # todo: クエリパラメータ以外の一般的なデータの渡し方を調査（余裕あれば）
        query_params: dict[str, str] = {
            "access": response.data["data"]["access"],
            "refresh": response.data["data"]["refresh"],
        }
        query_string = urlencode(query_params)
        return Response(
            status=status.HTTP_302_FOUND,
            headers={"Location": redirect_uri + "?" + query_string},
        )
