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

from accounts import constants as accounts_constants
from pong.custom_response import custom_response
from users.friends import constants as friends_constants

from .. import constants, serializers

logger = logging.getLogger(__name__)


class UsersMeView(views.APIView):
    """
    自分のユーザープロフィールを取得・更新する
    """

    # プロフィールを全て返すのでIsAuthenticatedをセットする必要がある
    permission_classes = [permissions.IsAuthenticated]

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
                                # todo: is_blocked,is_online,win_match,lose_match追加
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
        # リクエストのtokenからuserを取得
        user: User | AnonymousUser = request.user

        # AnonymousUserの場合はget()に入る前にpermission_classesで弾かれるが、
        # AnonymousUserだとuser.playerが使えずmypyでエラーになるため、事前にチェックが必要
        if not hasattr(user, "player"):
            # todo: この処理が必要ならlogger書く
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"user": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,  # todo: 404ではないかも。schemaに書いてない
            )

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
        request=utils.OpenApiRequest(
            serializers.UsersSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        accounts_constants.PlayerFields.DISPLAY_NAME: "new_name",
                        # todo: avatarも追加？
                    },
                ),
            ],
        ),
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
                                # todo: is_blocked,is_online,win_match,lose_match追加
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
        # リクエストのtokenからuserを取得
        user: User | AnonymousUser = request.user
        if not hasattr(user, "player"):
            # todo: この処理が必要ならlogger書く
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"user": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,  # todo: 404ではないかも。schemaに書いてない
            )
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
