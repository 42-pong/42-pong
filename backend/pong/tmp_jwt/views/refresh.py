import logging

from drf_spectacular import utils
from rest_framework import permissions, request, response, status, views
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from pong.custom_response import custom_response
from tmp_jwt import create_token_functions, jwt

logger = logging.getLogger(__name__)


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
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response (リクエスト形式が不正の場合)",
                        value={
                            "status": "error",
                            "code": "internal_error",
                        },
                    ),
                ],
            ),
            401: utils.OpenApiResponse(
                description="",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 401 response (トークンの形式が間違ってる場合)",
                        value={
                            "status": "error",
                            "code": "invalid",
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 401 response (リフレッシュトークンの有効期限が切れている場合)",
                        value={
                            "status": "error",
                            "code": "invalid",
                        },
                    ),
                ],
            ),
        },
    )
    def post(self, request: request.Request) -> response.Response:
        """
        リフレッシュトークンを使用して新しいアクセストークンを取得するPOSTメソッド
        """
        # todo: リフレッシュトークンを検証するシリアライズ作成
        required_keys: set = {"refresh"}
        request_keys: set = set(request.data.keys())
        if request_keys != required_keys:
            return custom_response.CustomResponse(
                code=["internal_error"],
                status=status.HTTP_400_BAD_REQUEST,
            )

        jwt_handler: jwt.JWT = jwt.JWT()
        refresh_token: str = request.data["refresh"]
        try:
            refresh_payload: dict = jwt_handler.decode(refresh_token)
        except Exception as e:
            logger.error(e)
            return custom_response.CustomResponse(
                code=["internal_error"],
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user_id = refresh_payload.get("sub")
        logger.debug(f"user_id: {user_id}")
        if user_id is None:
            logger.error("User ID missing in refresh token payload")
            return custom_response.CustomResponse(
                code=["internal_error"],
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token: str = create_token_functions.create_token(
            user_id, "access"
        )
        if not access_token:
            return custom_response.CustomResponse(
                code=["internal_error"],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return custom_response.CustomResponse(
            data={"access": access_token}, status=status.HTTP_200_OK
        )
