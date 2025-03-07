import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, views

from login import models, two_factor_auth
from pong.custom_response import custom_response

logger = logging.getLogger(__name__)


class LoginView(views.APIView):
    """
    アカウントが存在するかどうかを認証し、2要素認証用のパラメータを返すエンドポイント
    """

    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=utils.OpenApiRequest(
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
                response={
                    "type": "object",
                    "properties": {
                        "is_done_2fa": {
                            "type": "boolean",
                            "description": "2段階認証が有効かどうか",
                        },
                        "qr_code": {
                            "type": "string",
                            "description": "QRコードのURL",
                        },
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": {
                                "is_done_2fa": "false",
                                "qr_code": "/media/qr/qr_code.png",
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
    def post(self, request: request.Request) -> response.Response:
        """
        アカウントが存在するかどうかを認証し、2要素認証用のパラメータ生成するPOSTメソッド

        Responses:
            - 200: そのアカウントが2要素認証が有効かどうかを返す。無効の場合はQRコードのURLも返す
            - 400:
                - internal_error: リクエスト形式が不正の場合
            - 401:
                - not_exists: アカウントが存在しない場合
                - incorrect_password: パスワードが間違っている場合
            - 500:
                - internal_error:
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

        # 2要素認証のテーブル
        # - user_id
        # - secret
        # - is_done_2fa
        # userに紐づけていてる2要素認証のテーブルでis_done_two_fa2fa
        # falseの場合のみ
        # -> generate_2fa_qr_codeでsecretを生成し、2要素認証のテーブルにあるsecretを更新する
        two_fa, _ = models.TwoFactorAuth.objects.get_or_create(user=user)
        qr_code = ""
        if not two_fa.is_done_2fa:
            qr_code = f"/media/qr/{user.username}.png"
            two_fa.secret = two_factor_auth.generate_2fa_qr_code(
                user.email, "pong", qr_code
            )
            two_fa.save()
        return custom_response.CustomResponse(
            data={
                "is_done_2fa": two_fa.is_done_2fa,
                "qr_code": qr_code,
            },
            status=status.HTTP_200_OK,
        )
