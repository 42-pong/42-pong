from drf_spectacular import utils

# todo: IsAuthenticatedが追加されたらAllowAnyは不要かも
from rest_framework import permissions, request, response, status, views

from pong.custom_response import custom_response
from users import constants as users_constants

from . import constants
from .create_account import create_account
from .player import serializers as player_serializers
from .user import serializers as user_serializers


class AccountCreateView(views.APIView):
    """
    新規アカウントを作成するビュー
    """

    serializer_class: type[player_serializers.PlayerSerializer] = (
        player_serializers.PlayerSerializer
    )
    # todo: 認証機能を実装したら多分IsAuthenticatedに変更
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=utils.OpenApiRequest(
            player_serializers.PlayerSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        constants.PlayerFields.USER: {
                            constants.UserFields.EMAIL: "user@example.com",
                            constants.UserFields.PASSWORD: "password",
                        }
                    },
                ),
            ],
        ),
        responses={
            201: utils.OpenApiResponse(
                response=player_serializers.PlayerSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 201 response",
                        value={
                            "status": "ok",
                            "data": {
                                constants.UserFields.ID: 2,
                                constants.UserFields.USERNAME: "username",
                                constants.UserFields.EMAIL: "user@example.com",
                                constants.PlayerFields.DISPLAY_NAME: "default",
                                constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                users_constants.UsersFields.IS_FRIEND: False,
                                # todo: is_blocked,is_online,win_match,lose_match追加
                            },
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "status": {"type": ["string"]},
                        "errors": {"type": ["dict"]},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response",
                        value={
                            "status": "error",
                            "errors": {"field": ["error messages"]},
                        },
                    ),
                ],
            ),
        },
    )
    # todo: try-exceptを書いて予期せぬエラー(実装上のミスを含む)の場合に500を返す
    def post(
        self, request: request.Request, *args: tuple, **kwargs: dict
    ) -> response.Response:
        """
        新規アカウントを作成するPOSTメソッド
        requestをSerializerに渡してvalidationを行い、
        有効な場合はPlayerとUserを作成してDBに追加し、作成されたアカウント情報をresponseとして返す
        """

        def _create_user_serializer(
            user_data: dict,
        ) -> user_serializers.UserSerializer:
            # usernameのみBEがランダムな文字列をセット
            user_data[constants.UserFields.USERNAME] = (
                create_account.get_unique_random_username()
            )
            return user_serializers.UserSerializer(data=user_data)

        # サインアップ専用のUserSerializerを作成
        user_serializer: user_serializers.UserSerializer = _create_user_serializer(
            # popしたいfieldが存在しない場合は空dictを渡し、UserSerializerでエラーになる
            request.data.pop(constants.PlayerFields.USER, {})
        )
        if not user_serializer.is_valid():
            return custom_response.CustomResponse(
                errors=user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 作成したUserSerializerを使って新規アカウントを作成
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(
                user_serializer,
                request.data,
            )
        )
        if create_account_result.is_error:
            return custom_response.CustomResponse(
                errors=create_account_result.unwrap_error(),
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_serializer_data: dict = create_account_result.unwrap()
        return custom_response.CustomResponse(
            data=user_serializer_data,
            status=status.HTTP_201_CREATED,
        )
