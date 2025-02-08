from drf_spectacular import utils
from rest_framework import permissions, request, response, views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainView(views.APIView):
    """
    アクセストークンとリフレッシュトークンを取得するエンドポイント
    """

    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=TokenObtainPairSerializer,
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
        pass
        return response.Response()
