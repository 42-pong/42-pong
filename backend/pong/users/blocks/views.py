import logging

from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from django.db.models.query import QuerySet
from drf_spectacular import utils
from rest_framework import (
    exceptions,
    permissions,
    request,
    response,
    status,
    viewsets,
)

from accounts import constants as accounts_constants
from pong.custom_response import custom_response
from users import constants as users_constants

from . import constants, models
from .serializers import list_serializers

logger = logging.getLogger(__name__)


@utils.extend_schema_view(
    list=utils.extend_schema(
        responses={
            200: utils.OpenApiResponse(
                description="A list of blocks for the authenticated user.",
                response=list_serializers.BlockRelationshipListSerializer(
                    many=True
                ),
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: [
                                {
                                    constants.BlockRelationshipFields.BLOCKED_USER: {
                                        accounts_constants.UserFields.ID: 2,
                                        accounts_constants.UserFields.USERNAME: "username2",
                                        accounts_constants.PlayerFields.DISPLAY_NAME: "display_name2",
                                        accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                        users_constants.UsersFields.IS_FRIEND: False,
                                        # todo: is_blocked,is_online,win_match,lose_match追加
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
                                users_constants.Code.INTERNAL_ERROR
                            ],
                        },
                    ),
                ],
            ),
        },
    ),
)
class BlocksViewSet(viewsets.ViewSet):
    queryset = models.BlockRelationship.objects.filter(
        Q(blocked_user__player__isnull=False)
    ).select_related("user", "blocked_user")
    permission_classes = (permissions.IsAuthenticated,)

    http_method_names = ["get"]

    def handle_exception(self, exc: Exception) -> response.Response:
        """
        ModelViewSetのhandle_exception()をオーバーライド
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
                code=[users_constants.Code.INTERNAL_ERROR],
                errors={"detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )
        return response

    def _get_authenticated_user(self, user: User | AnonymousUser) -> User:
        """
        ログインユーザーを取得する
        AnonymousUserの場合は各メソッド関数関数に入る前にpermission_classesで弾かれるが、
        AnonymousUserだとuser.playerが使えずmypyでエラーになるため、事前にチェックが必要

        Raises:
            exceptions.NotAuthenticated: AnonymousUserの場合
        """
        if isinstance(user, AnonymousUser):
            raise exceptions.NotAuthenticated(
                "AnonymousUser is not authenticated."
            )
        return user

    # --------------------------------------------------------------------------
    # GET method
    # --------------------------------------------------------------------------
    def list(self, request: request.Request) -> response.Response:
        """
        ログインユーザーがブロックしているユーザープロフィール一覧を取得するGETメソッド
        """
        # ログインユーザーの取得
        user: User = self._get_authenticated_user(request.user)

        # 自分のブロック一覧を取得
        block_users: QuerySet[models.BlockRelationship] = self.queryset.filter(
            user=user
        )
        list_serializer: list_serializers.BlockRelationshipListSerializer = (
            list_serializers.BlockRelationshipListSerializer(
                block_users,
                many=True,
                context={constants.BlockRelationshipFields.USER_ID: user.id},
            )
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
        `/api/users/me/blocks/{blocked_user_id}/`,GETメソッド用の関数
        自動的に使用できるが仕様上不要なため、405を返しswagger-uiに表示されないようにしている
        """
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
