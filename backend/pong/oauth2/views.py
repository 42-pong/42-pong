# views.py
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from django.urls import reverse
from django.utils.crypto import get_random_string
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

from accounts import create_account
from pong import settings

from . import models, serializers


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

        oauth2_user_data: dict[str, str] = {
            # todo: 重複を防ぐget_random_stringのラッパー関数作成
            "username": get_random_string(12),
            "email": user_info.get("email"),
            # todo; パスワードは必須のため(仮)
            "password": "",
        }
        oauth2_user_serializer: serializers.UserSerializer = (
            serializers.UserSerializer(data=oauth2_user_data)
        )
        oauth2_user_serializer.is_valid(raise_exception=True)
        # todo: 42userのログイン名をplayer_dataに追加する
        player_data: dict = {}
        oauth2_user = create_account.create_account(
            oauth2_user_serializer, player_data
        )

        if oauth2_user.is_ok:
            user: models.User = oauth2_user.unwrap()
            # todo: user.idと必要な情報を使って、OAuth2とFortyTwoTokenのテーブルを作成する関数作成
            oauth2_data = {
                "user": user.id,
                "provider": "42",
                "provider_id": user_info.get("id"),
            }
            oauth2_serializer: serializers.OAuth2Serializer = (
                serializers.OAuth2Serializer(data=oauth2_data)
            )
            oauth2_serializer.is_valid(raise_exception=True)
            new_oauth2: models.OAuth2 = oauth2_serializer.save()
            forty_two_token_data = {
                "oauth2": new_oauth2.id,
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
            forty_two_token_serializer: serializers.FortyTwoTokenSerializer = (
                serializers.FortyTwoTokenSerializer(data=forty_two_token_data)
            )
            forty_two_token_serializer.is_valid(raise_exception=True)
            new_forty_two_token: models.FortyTwoToken = (
                forty_two_token_serializer.save()
            )
            # todo: 失敗した場合は、Userテーブルを削除する
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "oauth2": {
                        "id": new_oauth2.id,
                        "user_id": new_oauth2.user_id,
                        "provider": new_oauth2.provider,
                        "provider_id": new_oauth2.provider_id,
                    },
                    "token": {
                        "oauth2_id": new_forty_two_token.oauth2_id,
                        "access_token": new_forty_two_token.access_token,
                        "refresh_token": new_forty_two_token.refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

# todo: 以下のエンドポイントは後で実装する
# - oauth2/refresh
# - oauth2/revoke
# - oauth2/account
