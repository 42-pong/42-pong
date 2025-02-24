import logging
from typing import Optional

from django.contrib.auth.models import AnonymousUser, User
from django.db.models.query import QuerySet
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
from pong.custom_pagination import custom_pagination
from pong.custom_response import custom_response
from users.friends import constants as friends_constants

from .. import constants, serializers

logger = logging.getLogger(__name__)


class UsersListView(views.APIView):
    """
    ユーザープロフィールの一覧を取得するビュー
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

        if isinstance(exc, exceptions.NotFound):
            logger.error(f"[404] Not found: {str(exc)}")
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )

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
        AnonymousUserだとuser.id=Noneになるので先にエラーとして例外を発生させる

        Raises:
            exceptions.NotAuthenticated: AnonymousUserの場合
        """
        if isinstance(user, AnonymousUser):
            raise exceptions.NotAuthenticated(
                "AnonymousUser is not authenticated."
            )
        return user

    @utils.extend_schema(
        operation_id="get_users_list",
        request=None,
        parameters=[
            utils.OpenApiParameter(
                name="page",
                description="paginationのページ数",
                required=False,
                type=int,
                location=utils.OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: utils.OpenApiResponse(
                description="A list of user profiles",
                response=serializers.UsersSerializer(many=True),
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                custom_pagination.PaginationFields.COUNT: 25,
                                custom_pagination.PaginationFields.NEXT: "http://localhost:8000/api/users/?page=2",
                                custom_pagination.PaginationFields.PREVIOUS: None,
                                custom_pagination.PaginationFields.RESULTS: [
                                    {
                                        accounts_constants.UserFields.ID: 2,
                                        accounts_constants.UserFields.USERNAME: "username1",
                                        accounts_constants.PlayerFields.DISPLAY_NAME: "display_name1",
                                        accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample1.png",
                                        constants.UsersFields.IS_FRIEND: False,
                                        constants.UsersFields.IS_BLOCKED: False,
                                        # todo: is_online,win_match,lose_match追加
                                    },
                                    {
                                        accounts_constants.UserFields.ID: 3,
                                        accounts_constants.UserFields.USERNAME: "username2",
                                        accounts_constants.PlayerFields.DISPLAY_NAME: "display_name2",
                                        accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample2.png",
                                        constants.UsersFields.IS_FRIEND: False,
                                        constants.UsersFields.IS_BLOCKED: False,
                                        # todo: is_online,win_match,lose_match追加
                                    },
                                    "...",
                                ],
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
        ユーザープロフィール一覧を取得するGETメソッド
        """
        # ログインユーザーの取得
        user: User = self._get_authenticated_user(request.user)

        # Userに紐づくPlayer全てのQuerySetを取得
        all_players_with_users: QuerySet[player_models.Player] = (
            player_models.Player.objects.select_related(
                accounts_constants.PlayerFields.USER
            ).all()
        )
        paginator: custom_pagination.CustomPagination = (
            custom_pagination.CustomPagination()
        )
        # クエリパラメータのpage番号が存在しない場合はraise exceptions.NotFound()される
        paginated_players: Optional[list[player_models.Player]] = (
            paginator.paginate_queryset(all_players_with_users, request)
        )
        # 複数のオブジェクトをシリアライズ
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            paginated_players,
            many=True,
            # emailは含めない
            fields=(
                accounts_constants.UserFields.ID,
                accounts_constants.UserFields.USERNAME,
                accounts_constants.PlayerFields.DISPLAY_NAME,
                accounts_constants.PlayerFields.AVATAR,
                constants.UsersFields.IS_FRIEND,
                constants.UsersFields.IS_BLOCKED,
                # todo: is_online,win_match,lose_match追加
            ),
            context={friends_constants.FriendshipFields.USER_ID: user.id},
        )
        # todo: logger.info()追加
        return paginator.get_paginated_response(list(serializer.data))
