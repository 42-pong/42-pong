# views.py
from urllib.parse import urlencode

import requests
from django.urls import reverse
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status

# todo: IsAuthenticatedが追加されたらAllowAnyは不要?
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pong.settings import (
    OAUTH2_AUTHORIZATION_ENDPOINT,
    OAUTH2_CLIENT_ID,
    OAUTH2_CLIENT_SECRET_KEY,
    OAUTH2_TOKEN_ENDPOINT,
    PONG_ORIGIN,
)


class OAuth2BaseView(APIView):
    """
    OAuth2関連の共通の変数を定義する基底クラス
    """

    permission_classes = (AllowAny,)

    @property
    def redirect_uri(self) -> str:
        return PONG_ORIGIN + reverse("oauth2_callback")


class OAuth2AuthorizeView(OAuth2BaseView):
    @extend_schema(
        responses={
            302: OpenApiResponse(
                description="Redirect to OAuth2 authorization URL",
                examples=[
                    OpenApiExample(
                        "Example 302 Redirect",
                        value={
                            "Location": "https://example.com/oauth2/authorize?code=abc123..."
                        },
                    ),
                ],
            ),
        }
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
            "client_id": OAUTH2_CLIENT_ID,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
        }
        query_string: str = urlencode(query_params)

        authorization_url: str = (
            f"{OAUTH2_AUTHORIZATION_ENDPOINT}?{query_string}"
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
                        "Example 200 Response",
                        value={
                            "Token": {
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
                            "Token": {
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
            "client_id": OAUTH2_CLIENT_ID,
            "client_secret": OAUTH2_CLIENT_SECRET_KEY,
        }
        response: requests.models.Response = requests.post(
            OAUTH2_TOKEN_ENDPOINT,
            data=request_data,
        )
        tokens = response.json()
        return Response(
            {
                "Token": tokens,
            },
            status=response.status_code,
        )


# todo: 以下のエンドポイントは後で実装する
# - oauth2/refresh
# - oauth2/revoke
# - oauth2/account
