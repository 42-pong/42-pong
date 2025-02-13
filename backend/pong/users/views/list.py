from django.db.models.query import QuerySet
from drf_spectacular import utils
from rest_framework import (
    permissions,
    request,
    response,
    status,
    views,
)

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from pong.custom_response import custom_response

from .. import serializers


class UsersListView(views.APIView):
    """
    ユーザープロフィールの一覧を取得するビュー
    """

    # todo: IsAuthenticatedに変更する。extend_schemaにも401を追加する
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        operation_id="get_users_list",
        request=None,
        responses={
            200: utils.OpenApiResponse(
                description="A list of user profiles",
                response=serializers.UsersSerializer(many=True),
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: [
                                {
                                    accounts_constants.UserFields.ID: 2,
                                    accounts_constants.UserFields.USERNAME: "username1",
                                    accounts_constants.PlayerFields.DISPLAY_NAME: "display_name1",
                                    accounts_constants.PlayerFields.AVATAR: "avatars/sample1.png",
                                    # todo: is_friend,is_blocked,is_online,win_match,lose_match追加
                                },
                                {
                                    accounts_constants.UserFields.ID: 3,
                                    accounts_constants.UserFields.USERNAME: "username2",
                                    accounts_constants.PlayerFields.DISPLAY_NAME: "display_name2",
                                    accounts_constants.PlayerFields.AVATAR: "avatars/sample2.png",
                                    # todo: is_friend,is_blocked,is_online,win_match,lose_match追加
                                },
                                {"...", "..."},
                            ],
                        },
                    ),
                ],
            ),
            # todo: 詳細のschemaが必要であれば追加する
            500: utils.OpenApiResponse(description="Internal server error"),
        },
    )
    # todo: try-exceptで全体を囲って500を返す？
    def get(self, request: request.Request) -> response.Response:
        """
        ユーザープロフィール一覧を取得するGETメソッド
        """
        # Userに紐づくPlayer全てのQuerySetを取得
        all_players_with_users: QuerySet[player_models.Player] = (
            player_models.Player.objects.select_related(
                accounts_constants.PlayerFields.USER
            ).all()
        )
        # 複数のオブジェクトをシリアライズ
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            all_players_with_users,
            many=True,
            # emailは含めない
            fields=(
                accounts_constants.UserFields.ID,
                accounts_constants.UserFields.USERNAME,
                accounts_constants.PlayerFields.DISPLAY_NAME,
                accounts_constants.PlayerFields.AVATAR,
                # todo: is_friend,is_blocked,is_online,win_match,lose_match追加
            ),
        )
        return custom_response.CustomResponse(
            data=serializer.data, status=status.HTTP_200_OK
        )
