# views.py
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from django.urls import reverse
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

# todo: IsAuthenticatedが追加されたらAllowAnyは不要?
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pong import settings

from . import create_oauth2_account, models


class OAuth2BaseView(APIView):
    """
    OAuth2関連の共通の変数を定義する基底クラス
    """

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
    # todo callbackのエンドポイントのレスポンスが決まったら、request,responseを追加する
    @extend_schema(
        responses={
            200: OpenApiResponse(
                examples=[
                    OpenApiExample(
                        "Example 200 Response",
                        value={
                            "token": {
                                "access_token": "abc123",
                                "token_type": "bearer",
                                "expires_in": 3600,
                                "refresh_token": "abc123",
                                "scope": "public",
                                "created_at": 1734675524,
                                "secret_valid_until": 1736304711,
                            }
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
                description="Error when the provided authorization grant is invalid",
                examples=[
                    OpenApiExample(
                        "Example 401 Response",
                        value={
                            "token": {
                                "error": "invalid_grant",
                                "error_description": "The provided authorization grant is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client.",
                            }
                        },
                    )
                ],
            ),
            # todo: 他にもあるかも
        }
    )
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        認可サーバーからのレスポンスを受け取る関数
        この関数は認可エンドポイント(`/api/oauth2/authorize`)のレスポンスを受け取り、認可コードを取得するために使用する。
        そのため、このエンドポイントはFEから呼ばれることはありません。
        """
        # todo Optional[str]?
        code = request.GET.get("code")
        if not code:
            return Response(
                {
                    "error": "Authorization code is None. Please check your authentication process."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        user_response = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {tokens.get('access_token')}"},
        )
        user_info = user_response.json()

        oauth2_user_result: create_oauth2_account.CreateOAuth2UserResult = (
            create_oauth2_account.create_oauth2_user(
                user_info.get("email"), user_info.get("login")
            )
        )
        if not oauth2_user_result.is_ok:
            return Response(
                {"error": oauth2_user_result.unwrap_error()},
                status=status.HTTP_400_BAD_REQUEST,
            )
        oauth2_user: models.User = oauth2_user_result.unwrap()
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
        oauth2_result: create_oauth2_account.CreateFortyTwoAuthorizationResult = create_oauth2_account.create_forty_two_authorization(
            oauth2_user.id, user_info.get("id"), forty_two_token_data
        )
        # 42認証のテーブルが失敗した場合は、Userテーブルを削除する
        if not oauth2_result.is_ok:
            oauth2_user.delete()
            return Response(
                {"error": oauth2_result.unwrap_error()},
                status=status.HTTP_400_BAD_REQUEST,
            )
        oauth2: models.OAuth2 = oauth2_result.unwrap()
        # todo: oauth2_userをJWTに変換して返す
        return Response(
            {
                "user": {
                    "id": oauth2_user.id,
                    "username": oauth2_user.username,
                    "email": oauth2_user.email,
                },
                "oauth2": {
                    "id": oauth2.id,
                    "user_id": oauth2.user_id,
                    "provider": oauth2.provider,
                    "provider_id": oauth2.provider_id,
                },
            },
            status=status.HTTP_200_OK,
        )


# todo: 以下のエンドポイントは後で実装する
# - oauth2/refresh
# - oauth2/revoke
# - oauth2/account
