from django.db.models.query import QuerySet
from drf_spectacular import utils
from rest_framework import (
    permissions,
    request,
    response,
    status,
    views,
)

from accounts import constants
from accounts.player import models
from pong.custom_response import custom_response

from .. import serializers


class UsersListView(views.APIView):
    """
    ユーザープロフィールの一覧を取得するビュー
    """

    # todo: IsAuthenticatedに変更する
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=None,
        responses={
            200: utils.OpenApiResponse(
                description="A list of user profiles",
                response=serializers.UsersSerializer(many=True),
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": [
                                {
                                    "id": 2,
                                    "username": "username1",
                                    "display_name": "display_name1",
                                    # todo: avatar追加
                                },
                                {
                                    "id": 3,
                                    "username": "username2",
                                    "display_name": "display_name2",
                                    # todo: avatar追加
                                },
                                {"...", "..."},
                            ],
                        },
                    ),
                ],
            ),
        },
    )
    # todo: try-exceptで全体を囲って500を返す？
    def get(self, request: request.Request) -> response.Response:
        """
        ユーザープロフィール一覧を取得するGETメソッド
        """
        # Userに紐づくPlayer全てのQuerySetを取得
        all_players_with_users: QuerySet[models.Player] = (
            models.Player.objects.select_related(
                constants.PlayerFields.USER
            ).all()
        )
        # 複数のオブジェクトをシリアライズ
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            all_players_with_users, many=True
        )
        return custom_response.CustomResponse(
            data=serializer.data, status=status.HTTP_200_OK
        )
