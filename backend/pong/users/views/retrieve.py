import logging

from django.core.exceptions import ObjectDoesNotExist
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
from accounts.player import models as player_models
from pong.custom_response import custom_response
from users.friends import constants as friends_constants

from .. import constants, serializers

logger = logging.getLogger(__name__)


class UsersRetrieveView(views.APIView):
    """
    特定のuser_idのユーザープロフィールを取得するビュー
    """

    permission_classes = (permissions.IsAuthenticated,)

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
        operation_id="get_users_retrieve",
        request=None,
        responses={
            200: utils.OpenApiResponse(
                description="A user profile",
                response=serializers.UsersSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                accounts_constants.UserFields.ID: 2,
                                accounts_constants.UserFields.USERNAME: "username1",
                                accounts_constants.PlayerFields.DISPLAY_NAME: "display_name1",
                                accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                constants.UsersFields.IS_FRIEND: True,
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
            404: utils.OpenApiResponse(
                description="The user does not exist.",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.ERRORS: {"type": "list"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 404 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                constants.Code.INTERNAL_ERROR
                            ],
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
    def get(self, request: request.Request, user_id: int) -> response.Response:
        """
        特定のuser_idのユーザープロフィールを取得するGETメソッド

        Args:
            user_id: URLから取得したユーザーのID
        """
        try:
            # user_idに紐づくPlayerを取得
            player: player_models.Player = player_models.Player.objects.get(
                user_id=user_id
            )
        except ObjectDoesNotExist as e:
            # user_idに紐づくPlayerが存在しない場合
            logger.error(f"[404] {str(e)}: user_id={user_id} does not exist.")
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"user_id": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        users_serializer: serializers.UsersSerializer = (
            serializers.UsersSerializer(
                player,
                # emailは含めない
                fields=(
                    accounts_constants.UserFields.ID,
                    accounts_constants.UserFields.USERNAME,
                    accounts_constants.PlayerFields.DISPLAY_NAME,
                    accounts_constants.PlayerFields.AVATAR,
                    constants.UsersFields.IS_FRIEND,
                    # todo: is_blocked,is_online,win_match,lose_match追加
                ),
                context={
                    friends_constants.FriendshipFields.USER_ID: request.user.id
                },
            )
        )
        # todo: logger.info()追加
        return custom_response.CustomResponse(
            data=users_serializer.data,
            status=status.HTTP_200_OK,
        )
