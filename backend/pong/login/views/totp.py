import logging

from django.contrib.auth.models import User
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, views, test
from pong.custom_response import custom_response
from login import models, two_factor_auth
from jwt.views import token
from django.urls import reverse

logger = logging.getLogger(__name__)


class TotpView(views.APIView):
    """
    ワンタイムパスワードを検証し、アクセストークンとリフレッシュトークンを取得するエンドポイント
    """

    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=utils.OpenApiRequest(
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        "totp": "123456",
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
                        "Example 401 response (ワンタイムパスワードが間違っている場合)",
                        value={
                            "status": "error",
                            "code": "incorrect_password",
                        },
                    ),
                ],
            ),
            500: utils.OpenApiResponse(
                description="",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 500 response (予期せぬエラーの場合)",
                        value={
                            "status": "error",
                            "code": "internal_error",
                        },
                    ),
                ],
            ),
        },
    )
    def POST(self, request: request.Request) -> response.Response:
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
        required_keys: set = {"totp","email", "password"}
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
        two_fa = models.TwoFactorAuth.objects.get(user_id=user.id)
        secret = two_fa.secret
        totp = request.data["totp"]
        if (two_factor_auth.verify_2fa_otp(secret, totp)):
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
            return custom_response.CustomResponse(
                code=response.code,
                status=response.status_code,
                data=response.data,
            )

        if not two_fa.is_done_2fa:
            two_fa.is_done_2fa = True
            two_fa.save()
        return custom_response.CustomResponse(
            status=status.HTTP_200_OK, data=response.data
        )
