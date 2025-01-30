from drf_spectacular import utils
from rest_framework import (
    permissions,
    request,
    response,
    status,
    views,
)

from accounts.player import models
from pong.custom_response import custom_response

from .. import serializers


class UsersRetrieveView(views.APIView):
    """
    特定のuser_idのユーザープロフィールを取得するビュー
    """

    # todo: IsAuthenticatedに変更する
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=None,
        responses={
            200: utils.OpenApiResponse(
                description="A user profile",
                response=serializers.UsersSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": {
                                "id": 2,
                                "username": "username1",
                                "display_name": "display_name1",
                            },
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
        # todo: try-exceptで囲って404を返す
        # user_idに紐づくPlayerを取得
        player: models.Player = models.Player.objects.get(user_id=user_id)
        users_serializer: serializers.UsersSerializer = (
            serializers.UsersSerializer(player)
        )
        return custom_response.CustomResponse(
            data=users_serializer.data,
            status=status.HTTP_200_OK,
        )
