from django.contrib.auth.models import AnonymousUser, User
from drf_spectacular import utils
from rest_framework import (
    permissions,
    request,
    response,
    status,
    views,
)

from accounts import constants
from pong.custom_response import custom_response

from .. import serializers


class UsersMeView(views.APIView):
    """
    自分のユーザープロフィールを取得・更新する
    """

    permission_classes = [permissions.IsAuthenticated]

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
                                constants.UserFields.ID: 1,
                                constants.UserFields.USERNAME: "username1",
                                constants.PlayerFields.DISPLAY_NAME: "display_name1",
                            },
                        },
                    ),
                ],
            ),
        },
    )
    # todo: try-exceptで全体を囲って500を返す？
    def get(self, request: request.Request) -> response.Response:
        """
        自分のユーザープロフィールを取得するGETメソッド
        """
        # リクエストのtokenからuserを取得
        user: User | AnonymousUser = request.user
        users_serializer: serializers.UsersSerializer = (
            serializers.UsersSerializer(user.player)
        )
        return custom_response.CustomResponse(
            data=users_serializer.data,
            status=status.HTTP_200_OK,
        )

    # todo: PATCHメソッドを追加
