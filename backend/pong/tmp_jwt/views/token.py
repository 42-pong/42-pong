import logging

from django.contrib.auth.models import User
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from pong.custom_response import custom_response

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
        """
        # todo: JWT作成
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if user is None:
            logger.error(f"Email does not register: {email}")
            return custom_response.CustomResponse(
                code=["not_exists"], status=status.HTTP_401_UNAUTHORIZED
            )
        pass
        return response.Response()
        # 1. ユーザーが存在するかどうか
        # 2. パスワードが正しいかどうか
        # 3. user_idをペイロード作成
        # 4. ペイロードからJWTにエンコード
        # 5. アクセストークンとリフレッシュトークンを返す
        return custom_response.CustomResponse(status=status.HTTP_200_OK)
