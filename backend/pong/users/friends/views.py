import logging
from typing import Optional

from django.contrib.auth.models import AnonymousUser, User
from django.db import transaction
from django.db.models.query import QuerySet
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, viewsets

from accounts import constants as accounts_constants
from pong.custom_response import custom_response
from users import constants as users_constants

from . import constants, models
from .serializers import create_serializers, list_serializers

logger = logging.getLogger(__name__)


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
    create=utils.extend_schema(
        request=utils.OpenApiRequest(
            create_serializers.FriendshipCreateSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={constants.FriendshipFields.FRIEND_USER_ID: 1},
                ),
            ],
        ),
        responses={
            201: create_serializers.FriendshipCreateSerializer,
            400: utils.OpenApiResponse(
                description="The user does not exist.",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.CODE: {"type": "list"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response - not_exists",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: users_constants.Code.NOT_EXISTS,
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 400 response - invalid",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: users_constants.Code.INVALID,
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 400 response - internal_error",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: users_constants.Code.INTERNAL_ERROR,
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
        # todo: logger.info追加
        return custom_response.CustomResponse(
            data=list_serializer.data, status=status.HTTP_200_OK
        )

    @utils.extend_schema(exclude=True)
    def retrieve(
        self, request: request.Request, *args: tuple, **kwargs: dict
    ) -> response.Response:
        """
        `/api/users/me/friends/{friend_id}/`,GETメソッド用の関数
        自動的に使用できるが仕様上不要なため、405を返しswagger-uiに表示されないようにしている
        """
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _create_friendship_create_serializer(
        self, user_id: int, friend_user_id: Optional[int]
    ) -> create_serializers.FriendshipCreateSerializer:
        friendship_data: dict = {
            constants.FriendshipFields.USER_ID: user_id,
            constants.FriendshipFields.FRIEND_USER_ID: friend_user_id,
        }
        return create_serializers.FriendshipCreateSerializer(
            data=friendship_data
        )

    def _handle_create_validation_error(
        self, errors: dict, user_id: int, friend_user_id: Optional[int]
    ) -> response.Response:
        try:
            # friend_user_idしか入っていない想定のためignoreで対応
            code: str = errors.get(  # type: ignore
                constants.FriendshipFields.FRIEND_USER_ID
            )[0].code
            # codeの取得に成功した場合
            logger.error(
                f"[400] ValidationError: failed to create friendship(user_id={user_id},friend_user_id={friend_user_id}): code={code}: {errors}"
            )
            return custom_response.CustomResponse(
                code=[code],
                errors=errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as inner_exception:
            # codeの取得に失敗した場合
            logger.error(
                f"[500] Failed to create friendship(user_id={user_id},friend_user_id={friend_user_id}): {str(inner_exception)} from {errors}"
            )
            return custom_response.CustomResponse(
                code=[users_constants.Code.INTERNAL_ERROR],
                errors={"detail": str(inner_exception)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
        # Noneの場合はそのままserializerに渡してエラーになる
        friend_user_id: Optional[int] = request.data.get(
            constants.FriendshipFields.FRIEND_USER_ID
        )
        create_serializer: create_serializers.FriendshipCreateSerializer = (
            self._create_friendship_create_serializer(user.id, friend_user_id)
        )
        try:
            with transaction.atomic():
                if not create_serializer.is_valid():
                    return self._handle_create_validation_error(
                        create_serializer.errors, user.id, friend_user_id
                    )
                create_serializer.save()
            # todo: logger.info追加
            return custom_response.CustomResponse(
                data=create_serializer.data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # DatabaseErrorなど
            logger.error(
                f"[500] Failed to create friendship(user_id={user.id},friend_user_id={friend_user_id}): {str(e)}"
            )
            return custom_response.CustomResponse(
                code=[users_constants.Code.INTERNAL_ERROR],
                errors={"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
