import logging

from django.contrib.auth.models import AnonymousUser, User
from drf_spectacular import utils
from rest_framework import (
    exceptions,
    permissions,
    request,
    response,
    status,
    views,
)
from rest_framework.parsers import JSONParser, MultiPartParser

from accounts import constants as accounts_constants
from jwt.authentication import CustomJWTAuthentication
from pong.custom_response import custom_response
from users.friends import constants as friends_constants

from .. import constants, serializers

logger = logging.getLogger(__name__)


class UsersMeView(views.APIView):
    """
    自分のユーザープロフィールを取得・更新する
    """

    authentication_classes = [CustomJWTAuthentication]
    # プロフィールを全て返すのでIsAuthenticatedをセットする必要がある
    permission_classes = [permissions.IsAuthenticated]
    # アバター画像用にMultiPartParserを追加
    parser_classes = (JSONParser, MultiPartParser)

    def handle_exception(self, exc: Exception) -> response.Response:
        """
        APIViewのhandle_exception()をオーバーライド
        viewでtry-exceptしていない例外をカスタムレスポンスに変換して返す
        """
        if isinstance(
            exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)
        ):
            logger.error(f"[401] Authentication error: {str(exc)}")
            # 401はCustomResponseにせずそのまま返す
            return super().handle_exception(exc)

        logger.error(f"[500] Internal server error: {str(exc)}")
        response: custom_response.CustomResponse = (
            custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )
        return response

    def _get_authenticated_user(self, user: User | AnonymousUser) -> User:
        """
        ログインユーザーを取得する
        AnonymousUserの場合は各メソッド関数関数に入る前にpermission_classesで弾かれるはずだが、
        AnonymousUserだとuser.id=Noneになったりuser.playerが使えずmypyでエラーになったりするため、
        先にエラーとして例外を発生させる

        Raises:
            exceptions.NotAuthenticated: AnonymousUserの場合
        """
        if isinstance(user, AnonymousUser):
            raise exceptions.NotAuthenticated(
                "AnonymousUser is not authenticated."
            )
        return user

    @utils.extend_schema(
        request=None,
        responses={
            200: utils.OpenApiResponse(
                description="My user profile",
                response=serializers.UsersSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                accounts_constants.UserFields.ID: 1,
                                accounts_constants.UserFields.USERNAME: "username1",
                                accounts_constants.UserFields.EMAIL: "username1@example.com",
                                accounts_constants.PlayerFields.DISPLAY_NAME: "display_name1",
                                accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                constants.UsersFields.IS_FRIEND: False,
                                constants.UsersFields.IS_BLOCKED: False,
                                constants.UsersFields.MATCH_WINS: 1,
                                constants.UsersFields.MATCH_LOSSES: 0,
                            },
                        },
                    ),
                ],
            ),
            # todo: 現在Djangoが自動で返している。CustomResponseが使えたら併せて変更する
            401: utils.OpenApiResponse(
                description="Not authenticated",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 401 response",
                        value={
                            "detail": "Authentication credentials were not provided."
                        },
                    ),
                ],
            ),
            500: utils.OpenApiResponse(
                description="Internal server error",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.CODE: {"type": "list"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 500 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                constants.Code.INTERNAL_ERROR
                            ],
                        },
                    ),
                ],
            ),
        },
    )
    def get(self, request: request.Request) -> response.Response:
        """
        自分のユーザープロフィールを取得するGETメソッド
        """
        # ログインユーザーの取得
        user: User = self._get_authenticated_user(request.user)
        # serializer作成
        users_serializer: serializers.UsersSerializer = (
            serializers.UsersSerializer(
                user.player,
                # 全て取得するのでfieldsは指定しない
                context={friends_constants.FriendshipFields.USER_ID: user.id},
            )
        )
        # todo: logger.info()追加
        return custom_response.CustomResponse(
            data=users_serializer.data,
            status=status.HTTP_200_OK,
        )

    @utils.extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    accounts_constants.PlayerFields.DISPLAY_NAME: {
                        "type": "string",
                        "example": "new_name",
                    },
                },
            },
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    accounts_constants.PlayerFields.AVATAR: {
                        "type": "string",
                        "format": "binary",
                        "example": "example.png",
                    },
                },
            },
        },
        responses={
            200: utils.OpenApiResponse(
                description="My user profile",
                response=serializers.UsersSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                accounts_constants.UserFields.ID: 1,
                                accounts_constants.UserFields.USERNAME: "username1",
                                accounts_constants.UserFields.EMAIL: "username1@example.com",
                                accounts_constants.PlayerFields.DISPLAY_NAME: "display_name1",
                                accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                constants.UsersFields.IS_FRIEND: False,
                                constants.UsersFields.IS_BLOCKED: False,
                                constants.UsersFields.MATCH_WINS: 1,
                                constants.UsersFields.MATCH_LOSSES: 0,
                            },
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                description="Validation error",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.CODE: {"type": "list"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [constants.Code.INVALID],
                        },
                    ),
                ],
            ),
            # todo: 現在Djangoが自動で返している。CustomResponseが使えたら併せて変更する
            401: utils.OpenApiResponse(
                description="Not authenticated",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 401 response",
                        value={
                            "detail": "Authentication credentials were not provided."
                        },
                    ),
                ],
            ),
            500: utils.OpenApiResponse(
                description="Internal server error",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.CODE: {"type": "list"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 500 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                constants.Code.INTERNAL_ERROR
                            ],
                        },
                    ),
                ],
            ),
        },
    )
    def patch(self, request: request.Request) -> response.Response:
        """
        自分のユーザープロフィールを更新するPATCHメソッド
        """
        # ログインユーザーの取得
        user: User = self._get_authenticated_user(request.user)
        # serializer作成
        users_serializer: serializers.UsersSerializer = (
            serializers.UsersSerializer(
                user.player,
                data=request.data,
                partial=True,  # 部分的な更新を許可
                # 全て取得するのでfieldsは指定しない
                context={friends_constants.FriendshipFields.USER_ID: user.id},
            )
        )
        # 更新対象データ(request.data)のバリデーションを確認
        if not users_serializer.is_valid():
            logger.error(
                f"[400] Serializer's validation error: {users_serializer.errors}"
            )
            return custom_response.CustomResponse(
                code=[constants.Code.INVALID],
                errors=users_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 更新
        users_serializer.save()
        # todo: logger.info()追加
        return custom_response.CustomResponse(
            data=users_serializer.data,
            status=status.HTTP_200_OK,
        )
