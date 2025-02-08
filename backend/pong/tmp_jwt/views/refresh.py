from drf_spectacular import utils
from rest_framework import permissions, request, response, views
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class TokenRefreshView(views.APIView):
    """
    リフレッシュトークンを使用して新しいアクセストークンを取得するエンドポイント
    """

    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=TokenRefreshSerializer,
        responses={
            200: utils.OpenApiResponse(
                description="新しいアクセストークンを返す",
                response={
                    "type": "object",
                    "properties": {
                        "access": {
                            "type": "string",
                            "description": "新しいアクセストークン",
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
                            },
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                description="リクエスト形式が不正の場合",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response",
                        value={
                            "status": "error",
                            "code": "invalid_request",
                        },
                    ),
                ],
            ),
            401: utils.OpenApiResponse(
                description="トークンの形式が間違っている、またはリフレッシュトークンの有効期限が切れている場合",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 401 response (invalid token format)",
                        value={
                            "status": "error",
                            "code": "invalid_token_format",
                        },
                        description="トークンの形式が間違っています",
                    ),
                    utils.OpenApiExample(
                        "Example 401 response (refresh token expired)",
                        value={
                            "status": "error",
                            "code": "refresh_token_expired",
                        },
                        description="リフレッシュトークンの有効期限が切れています。再度ログインをしてください。",
                    ),
                ],
            ),
        },
    )
    def post(self, request: request.Request) -> response.Response:
        """
        リフレッシュトークンを使用して新しいアクセストークンを取得するPOSTメソッド
        """
        pass
        return response.Response()
