import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from pong.custom_response import custom_response
from tmp_jwt import create_token_functions

logger = logging.getLogger(__name__)


class TokenObtainView(views.APIView):
    """
    アクセストークンとリフレッシュトークンを取得するエンドポイント
    """

    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=utils.OpenApiRequest(
            TokenObtainPairSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        "email": "user@example.com",
                        "password": "password",
                    },
                ),
            ],
        ),
        responses={
            200: utils.OpenApiResponse(
                description="アクセストークンとリフレッシュトークンを返す",
                response={
                    "type": "object",
                    "properties": {
                        "access": {
                            "type": "string",
                            "description": "アクセストークン",
                        },
                        "refresh": {
                            "type": "string",
                            "description": "リフレッシュトークン",
                        },
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": {
                                "access": "eyJhbGciOiJIUzI1...",
                                "refresh": "eyJhbGciOiJIUzI1...",
                            },
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response(リクエスト形式が不正の場合)",
                        value={
                            "status": "error",
                            "code": "internal_error",
                        },
                    ),
                ],
            ),
            401: utils.OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 401 response (アカウントが存在しない場合)",
                        value={
                            "status": "error",
                            "code": "not_exists",
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 401 response (パスワードが間違っている場合)",
                        value={
                            "status": "error",
                            "code": "incorrect_password",
                        },
                    ),
                ],
            ),
        },
    )
    def post(self, request: request.Request) -> response.Response:
        """
        アクセストークンとリフレッシュトークンを取得するPOSTメソッド

        Responses:
            - 200: アクセストークンとリフレッシュトークンを返す
            - 400:
                - internal_error: リクエスト形式が不正の場合
            - 401:
                - not_exists: アカウントが存在しない場合
                - incorrect_password: パスワードが間違っている場合
            - 500:
                - internal_error:
                    - JWTトークンの生成に失敗した場合
                    - 予期せぬエラーが発生した場合
        """
        required_keys: set = {"email", "password"}
        request_keys: set = set(request.data.keys())
        if request_keys != required_keys:
            return custom_response.CustomResponse(
                code=["internal_error"],
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if user is None:
            logger.error(f"Email does not register: {email}")
            return custom_response.CustomResponse(
                code=["not_exists"], status=status.HTTP_401_UNAUTHORIZED
            )

        password = request.data.get("password")
        if authenticate(username=user.username, password=password) is None:
            logger.error("Password is incorrect")
            return custom_response.CustomResponse(
                code=["incorrect_password"],
                status=status.HTTP_401_UNAUTHORIZED,
            )

        tokens: dict = create_token_functions.create_access_and_refresh_token(
            user.id
        )
        if not tokens["access"] or not tokens["refresh"]:
            return custom_response.CustomResponse(
                code=["internal_error"],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return custom_response.CustomResponse(
            data=tokens, status=status.HTTP_200_OK
        )
