import logging

from django.contrib.auth.models import User
from django.urls import reverse
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, test, views

from jwt.views import token
from login import models, serializers, two_factor_auth
from pong.custom_response import custom_response

logger = logging.getLogger(__name__)


class TotpView(views.APIView):
    """
    ワンタイムパスワードを検証し、アクセストークンとリフレッシュトークンを取得するエンドポイント
    """

    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=serializers.TotpSerializer,
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
                    "properties": {
                        "status": {"type": "string"},
                        "code": {"type": "array", "items": {"type": "string"}},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response(リクエスト形式が不正の場合)",
                        value={
                            "status": "error",
                            "code": ["internal_error"],
                        },
                    ),
                ],
            ),
            401: utils.OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "code": {"type": "array", "items": {"type": "string"}},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 401 response (ワンタイムパスワードが間違っている場合)",
                        value={
                            "status": "error",
                            "code": ["incorrect_password"],
                        },
                    ),
                ],
            ),
            500: utils.OpenApiResponse(
                description="",
                response={
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "code": {"type": "array", "items": {"type": "string"}},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 500 response (予期せぬエラーの場合)",
                        value={
                            "status": "error",
                            "code": ["internal_error"],
                        },
                    ),
                ],
            ),
        },
    )
    def post(self, request: request.Request) -> response.Response:
        """
        ワンタイムパスワードを検証し、アクセストークンとリフレッシュトークンを生成するPOSTメソッド

        Responses:
            - 200: アクセストークンとリフレッシュトークンを返す
            - 400:
                - internal_error: リクエスト形式が不正の場合
            - 401:
                - incorrect_password: ワンタイムパスワードが間違っている場合
            - 500:
                - internal_error:
                    - 予期せぬエラーが発生した場合
        """
        required_keys: set = {"totp", "email", "password"}
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
        totp = request.data.get("totp")
        if not totp:
            logger.error(f"TOTP fail: {totp}")
            return custom_response.CustomResponse(
                code=["fail"], status=status.HTTP_401_UNAUTHORIZED
            )

        two_fa = models.TwoFactorAuth.objects.filter(user_id=user.id).first()
        if two_fa is None:
            logger.error(f"2fa does not register: {email}")
            return custom_response.CustomResponse(
                code=["not_exists"], status=status.HTTP_401_UNAUTHORIZED
            )

        secret = two_fa.secret
        if secret is None:
            logger.error(f"Secret not found for user {user.id}")
            return custom_response.CustomResponse(
                code=["fail"], status=status.HTTP_401_UNAUTHORIZED
            )

        if not two_factor_auth.verify_2fa_totp(secret, totp):
            return custom_response.CustomResponse(
                code=["incorrect_password"],
                status=status.HTTP_401_UNAUTHORIZED,
            )

        password = request.data.get("password")
        factory = test.APIRequestFactory()
        request = factory.post(
            reverse("jwt:token_obtain_pair"),
            {
                "email": user.email,
                "password": password,
            },
            format="json",
        )
        response = token.TokenObtainView.as_view()(request)
        if response.status_code != status.HTTP_200_OK:
            logger.error(
                f"{response.status_code} TokenObtainFailedError: {response.data}"
            )
            return response

        if not two_fa.is_done_2fa:
            two_fa.is_done_2fa = True
            two_fa.save()
        return response
