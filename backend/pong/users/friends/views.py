from typing import Optional

from django.contrib.auth.models import AnonymousUser, User
from django.db.models.query import QuerySet
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, viewsets

from accounts import constants as accounts_constants
from pong.custom_response import custom_response
from users import constants as users_constants

from . import constants, models
from .serializers import create_serializers, list_serializers


@utils.extend_schema_view(
    list=utils.extend_schema(
        responses={
            200: utils.OpenApiResponse(
                description="A list of friends for the authenticated user.",
                response=list_serializers.FriendshipListSerializer(many=True),
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: [
                                {
                                    constants.FriendshipFields.USER_ID: 1,
                                    constants.FriendshipFields.FRIEND_USER_ID: 2,
                                    constants.FriendshipFields.FRIEND: {
                                        accounts_constants.UserFields.USERNAME: "username2",
                                        accounts_constants.PlayerFields.DISPLAY_NAME: "display_name2",
                                        accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                    },
                                },
                                {"...", "..."},
                            ],
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
            # todo: 404は確定したら追加する
            # todo: 詳細のschemaが必要であれば追加する
            500: utils.OpenApiResponse(description="Internal server error"),
        },
    ),
)
# todo: 各メソッドにtry-exceptを書いて予期せぬエラー(実装上のミスを含む)の場合に500を返す
class FriendsViewSet(viewsets.ModelViewSet):
    queryset = models.Friendship.objects.all().select_related("user", "friend")
    permission_classes = (permissions.IsAuthenticated,)

    # URLから取得するID名
    lookup_field = "friend_id"

    http_method_names = ["get", "post"]

    def list(self, request: request.Request) -> response.Response:
        """
        自分のフレンドのユーザープロフィール一覧を取得するGETメソッド
        """
        user: User | AnonymousUser = request.user
        if isinstance(user, AnonymousUser):
            return custom_response.CustomResponse(
                code=[users_constants.Code.INTERNAL_ERROR],
                errors={"user": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,  # todo: 404ではないかも
            )

        # 自分のフレンド一覧を取得
        friends: QuerySet[models.Friendship] = self.queryset.filter(user=user)
        list_serializer: list_serializers.FriendshipListSerializer = (
            list_serializers.FriendshipListSerializer(friends, many=True)
        )
        return custom_response.CustomResponse(
            data=list_serializer.data, status=status.HTTP_200_OK
        )

    def _create_friendship_create_serializer(
        self, request_data: dict, user_id: int
    ) -> create_serializers.FriendshipCreateSerializer:
        # Noneの場合はそのままserializerに渡してエラーになる
        friend_user_id: Optional[int] = request_data.get(
            constants.FriendshipFields.FRIEND_USER_ID
        )
        friendship_data: dict = {
            constants.FriendshipFields.USER_ID: user_id,
            constants.FriendshipFields.FRIEND_USER_ID: friend_user_id,
        }
        return create_serializers.FriendshipCreateSerializer(
            data=friendship_data
        )

    def create(self, request: request.Request) -> response.Response:
        """
        自分のフレンドに特定の新しいユーザーを追加するPOSTメソッド
        """

        # ログインユーザーの取得
        user: User | AnonymousUser = request.user
        if isinstance(user, AnonymousUser):
            return custom_response.CustomResponse(
                code=[users_constants.Code.INTERNAL_ERROR],
                errors={"user": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,  # todo: 404ではないかも
            )

        create_serializer: create_serializers.FriendshipCreateSerializer = (
            self._create_friendship_create_serializer(
                request.data, request.user.id
            )
        )
        # todo: try-except
        create_serializer.is_valid(raise_exception=True)
        create_serializer.save()
        return custom_response.CustomResponse(
            data=create_serializer.data, status=status.HTTP_201_CREATED
        )
