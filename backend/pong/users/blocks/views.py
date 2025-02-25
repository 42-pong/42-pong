import logging
from typing import Optional

import rest_framework_simplejwt
from django.contrib.auth.models import AnonymousUser, User
from django.db import transaction
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
from pong.custom_pagination import custom_pagination
from pong.custom_response import custom_response
from users import constants as users_constants

from . import constants, models
from .serializers import (
    create_serializers,
    destroy_serializers,
    list_serializers,
)

logger = logging.getLogger(__name__)


@utils.extend_schema_view(
    list=utils.extend_schema(
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
                description="A list of blocks for the authenticated user.",
                response=list_serializers.BlockRelationshipListSerializer(
                    many=True
                ),
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                custom_pagination.PaginationFields.COUNT: 25,
                                custom_pagination.PaginationFields.NEXT: "http://localhost:8000/api/users/me/blocks/?page=2",
                                custom_pagination.PaginationFields.PREVIOUS: None,
                                custom_pagination.PaginationFields.RESULTS: [
                                    {
                                        constants.BlockRelationshipFields.BLOCKED_USER: {
                                            accounts_constants.UserFields.ID: 2,
                                            accounts_constants.UserFields.USERNAME: "username2",
                                            accounts_constants.PlayerFields.DISPLAY_NAME: "display_name2",
                                            accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                            users_constants.UsersFields.IS_FRIEND: False,
                                            users_constants.UsersFields.IS_BLOCKED: True,
                                            # todo: is_online,win_match,lose_match追加
                                        },
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
                                users_constants.Code.INTERNAL_ERROR
                            ],
                        },
                    ),
                ],
            ),
        },
    ),
    create=utils.extend_schema(
        request=utils.OpenApiRequest(
            create_serializers.BlockRelationshipCreateSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        constants.BlockRelationshipFields.BLOCKED_USER_ID: 1
                    },
                ),
            ],
        ),
        responses={
            201: utils.OpenApiResponse(
                description="Successfully added a new user to the authenticated user's block list.",
                response=create_serializers.BlockRelationshipCreateSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 201 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                constants.BlockRelationshipFields.BLOCKED_USER: {
                                    accounts_constants.UserFields.ID: 2,
                                    accounts_constants.UserFields.USERNAME: "username2",
                                    accounts_constants.PlayerFields.DISPLAY_NAME: "display_name2",
                                    accounts_constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                    users_constants.UsersFields.IS_FRIEND: False,
                                    users_constants.UsersFields.IS_BLOCKED: True,
                                    # todo: is_online,win_match,lose_match追加
                                },
                            },
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                description="Invalid blocked_user_id (複数例あり)",
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
                            custom_response.CODE: [
                                users_constants.Code.NOT_EXISTS
                            ],
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 400 response - invalid",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                users_constants.Code.INVALID
                            ],
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 400 response - internal_error",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                users_constants.Code.INTERNAL_ERROR
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
    destroy=utils.extend_schema(
        request=destroy_serializers.BlockRelationshipDestroySerializer,
        responses={
            204: None,
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
                description="Invalid blocked_user_id (複数例あり)",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.CODE: {"type": "list"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 404 response - not_exists",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                users_constants.Code.NOT_EXISTS
                            ],
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 404 response - invalid",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                users_constants.Code.INVALID
                            ],
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 404 response - internal_error",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                users_constants.Code.INTERNAL_ERROR
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

    # todo: 自作JWTの認証クラスを設定する
    authentication_classes = [
        rest_framework_simplejwt.authentication.JWTAuthentication
    ]
    permission_classes = (permissions.IsAuthenticated,)

    # URLから取得するID名
    lookup_field = constants.BlockRelationshipFields.BLOCKED_USER_ID

    http_method_names = ["get", "post", "delete"]

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

        if isinstance(exc, exceptions.NotFound):
            logger.error(f"[404] Not found: {str(exc)}")
            return custom_response.CustomResponse(
                code=[users_constants.Code.INTERNAL_ERROR],
                errors={"detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )

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
        paginator: custom_pagination.CustomPagination = (
            custom_pagination.CustomPagination()
        )
        # クエリパラメータのpage番号が存在しない場合はraise exceptions.NotFound()される
        paginated_block_users: Optional[list[models.BlockRelationship]] = (
            paginator.paginate_queryset(block_users, request)
        )
        list_serializer: list_serializers.BlockRelationshipListSerializer = (
            list_serializers.BlockRelationshipListSerializer(
                paginated_block_users,
                many=True,
                context={constants.BlockRelationshipFields.USER_ID: user.id},
            )
        )
        # todo: logger.info追加
        return paginator.get_paginated_response(list(list_serializer.data))

    @utils.extend_schema(exclude=True)
    def retrieve(
        self, request: request.Request, *args: tuple, **kwargs: dict
    ) -> response.Response:
        """
        `/api/users/me/blocks/{blocked_user_id}/`,GETメソッド用の関数
        自動的に使用できるが仕様上不要なため、405を返しswagger-uiに表示されないようにしている
        """
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # --------------------------------------------------------------------------
    # POST method
    # --------------------------------------------------------------------------
    def _create_block_relationship_serializer(
        self, user_id: int, blocked_user_id: Optional[int]
    ) -> create_serializers.BlockRelationshipCreateSerializer:
        block_relationship_data: dict = {
            constants.BlockRelationshipFields.BLOCKED_USER_ID: blocked_user_id
        }
        return create_serializers.BlockRelationshipCreateSerializer(
            data=block_relationship_data,
            context={constants.BlockRelationshipFields.USER_ID: user_id},
        )

    def _handle_create_validation_error(
        self, errors: dict, user_id: int, blocked_user_id: Optional[int]
    ) -> response.Response:
        try:
            # blocked_user_idしか入っていない想定のためignoreで対応
            code: str = errors.get(  # type: ignore
                constants.BlockRelationshipFields.BLOCKED_USER_ID
            )[0].code
            # codeの取得に成功した場合
            logger.error(
                f"[400] ValidationError: failed to create block_relationship\
                (user_id={user_id},blocked_user_id={blocked_user_id}): code={code}: {errors}"
            )
            return custom_response.CustomResponse(
                code=[code],
                errors=errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # codeの取得に失敗した場合
            logger.error(
                f"[500] Failed to create block_relationship\
                (user_id={user_id},blocked_user_id={blocked_user_id}): {str(e)} from {errors}"
            )
            raise

    def create(self, request: request.Request) -> response.Response:
        """
        自分のブロックリストに特定の新しいユーザーを追加するPOSTメソッド
        """
        # ログインユーザーの取得
        user: User = self._get_authenticated_user(request.user)

        # Noneの場合はそのままserializerに渡してエラーになる
        blocked_user_id: Optional[int] = request.data.get(
            constants.BlockRelationshipFields.BLOCKED_USER_ID
        )
        create_serializer: create_serializers.BlockRelationshipCreateSerializer = self._create_block_relationship_serializer(
            user.id, blocked_user_id
        )
        try:
            with transaction.atomic():
                if not create_serializer.is_valid():
                    return self._handle_create_validation_error(
                        create_serializer.errors, user.id, blocked_user_id
                    )
                create_serializer.save()
            # todo: logger.info追加
            return custom_response.CustomResponse(
                data=create_serializer.data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # DatabaseErrorなど
            logger.error(
                f"[500] Failed to create block_relationship\
                (user_id={user.id},blocked_user_id={blocked_user_id}): {str(e)}"
            )
            raise

    # --------------------------------------------------------------------------
    # DELETE method
    # --------------------------------------------------------------------------
    def _create_destroy_serializer(
        self, user_id: int, blocked_user_id: int
    ) -> destroy_serializers.BlockRelationshipDestroySerializer:
        block_relationship_data: dict = {
            constants.BlockRelationshipFields.BLOCKED_USER_ID: blocked_user_id
        }
        return destroy_serializers.BlockRelationshipDestroySerializer(
            data=block_relationship_data,
            context={constants.BlockRelationshipFields.USER_ID: user_id},
        )

    def _handle_destroy_validation_error(
        self, errors: dict, user_id: int, blocked_user_id: int
    ) -> response.Response:
        try:
            # blocked_user_idしか入っていない想定のためignoreで対応
            code: str = errors.get(  # type: ignore
                constants.BlockRelationshipFields.BLOCKED_USER_ID
            )[0].code
            logger.error(
                f"[404] ValidationError: failed to delete block_relationship\
                (user_id={user_id},blocked_user_id={blocked_user_id}): {errors}"
            )
            return custom_response.CustomResponse(
                # "not_exists" or "invalid" or "internal_error"
                code=[code],
                errors=errors,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # codeの取得に失敗した場合
            logger.error(
                f"[500] Failed to delete block_relationship\
                (user_id={user_id},blocked_user_id={blocked_user_id}): {str(e)} from {errors}"
            )
            raise

    def destroy(
        self, request: request.Request, blocked_user_id: int
    ) -> response.Response:
        """
        自分のブロックリストから特定のユーザーを削除するDELETEメソッド
        """
        # ログインユーザーの取得
        user: User = self._get_authenticated_user(request.user)

        destroy_serializer: destroy_serializers.BlockRelationshipDestroySerializer = self._create_destroy_serializer(
            user.id, blocked_user_id
        )
        try:
            with transaction.atomic():
                if not destroy_serializer.is_valid():
                    return self._handle_destroy_validation_error(
                        destroy_serializer.errors, user.id, blocked_user_id
                    )
                block_relationship: models.BlockRelationship = (
                    models.BlockRelationship.objects.get(
                        user_id=user.id, blocked_user_id=blocked_user_id
                    )
                )
                block_relationship.delete()
            # todo: logger.info追加
            return custom_response.CustomResponse(
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            # DatabaseErrorなど
            logger.error(
                f"[500] Failed to delete block_relationship\
                (user_id={user.id},blocked_user_id={blocked_user_id}): {str(e)}"
            )
            raise
