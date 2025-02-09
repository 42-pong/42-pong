import logging

from django.contrib.auth.models import AnonymousUser, User
from drf_spectacular import utils
from rest_framework import (
    permissions,
    request,
    response,
    status,
    views,
)

from accounts import constants as accounts_constants
from pong.custom_response import custom_response

from .. import constants, serializers

logger = logging.getLogger(__name__)


class UsersMeView(views.APIView):
    """
    自分のユーザープロフィールを取得・更新する
    """

    # プロフィールを全て返すのでIsAuthenticatedをセットする必要がある
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
                                accounts_constants.UserFields.ID: 1,
                                accounts_constants.UserFields.USERNAME: "username1",
                                accounts_constants.UserFields.EMAIL: "username1@example.com",
                                accounts_constants.PlayerFields.DISPLAY_NAME: "display_name1",
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
            # todo: 詳細のschemaが必要であれば追加する
            500: utils.OpenApiResponse(description="Internal server error"),
        },
    )
    # todo: try-exceptで全体を囲って500を返す？
    def get(self, request: request.Request) -> response.Response:
        """
        自分のユーザープロフィールを取得するGETメソッド
        """
        # リクエストのtokenからuserを取得
        user: User | AnonymousUser = request.user

        # AnonymousUserの場合はget()に入る前にpermission_classesで弾かれるが、
        # AnonymousUserだとuser.playerが使えずmypyでエラーになるため、事前にチェックが必要
        if not hasattr(user, "player"):
            # todo: この処理が必要ならlogger書く
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"user": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,  # todo: 404ではないかも。schemaに書いてない
            )

        users_serializer: serializers.UsersSerializer = (
            serializers.UsersSerializer(user.player)
        )
        return custom_response.CustomResponse(
            data=users_serializer.data,
            status=status.HTTP_200_OK,
        )

    @utils.extend_schema(
        request=utils.OpenApiRequest(
            serializers.UsersSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        accounts_constants.PlayerFields.DISPLAY_NAME: "new_name",
                    },
                ),
            ],
        ),
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
                                accounts_constants.UserFields.ID: 1,
                                accounts_constants.UserFields.USERNAME: "username1",
                                accounts_constants.UserFields.EMAIL: "username1@example.com",
                                accounts_constants.PlayerFields.DISPLAY_NAME: "display_name1",
                            },
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                description="Validation error",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.ERRORS: {"type": "dict"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [constants.Code.INVALID],
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
            # todo: 詳細のschemaが必要であれば追加する
            500: utils.OpenApiResponse(description="Internal server error"),
        },
    )
    # todo: try-exceptで全体を囲って500を返す
    def patch(self, request: request.Request) -> response.Response:
        """
        自分のユーザープロフィールを更新するPATCHメソッド
        """
        # リクエストのtokenからuserを取得
        user: User | AnonymousUser = request.user
        if not hasattr(user, "player"):
            # todo: この処理が必要ならlogger書く
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"user": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,  # todo: 404ではないかも。schemaに書いてない
            )
        # serializer作成
        users_serializer: serializers.UsersSerializer = (
            serializers.UsersSerializer(
                user.player,
                data=request.data,
                partial=True,  # 部分的な更新を許可
            )
        )
        # 更新対象データ(request.data)のバリデーションを確認
        if not users_serializer.is_valid():
            logger.error(
                f"[400] Serializer's validation error: {users_serializer.errors}"
            )
            return custom_response.CustomResponse(
                code=[constants.Code.INVALID],
                errors=users_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 更新
        users_serializer.save()
        return custom_response.CustomResponse(
            data=users_serializer.data,
            status=status.HTTP_200_OK,
        )
