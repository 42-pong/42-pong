from drf_spectacular import utils

# todo: IsAuthenticatedが追加されたらAllowAnyは不要かも
from rest_framework import permissions, request, response, status, views

from pong.custom_response import custom_response

from . import constants, create_account, serializers


class AccountCreateView(views.APIView):
    """
    新規アカウントを作成するビュー
    """

    serializer_class: type[serializers.PlayerSerializer] = (
        serializers.PlayerSerializer
    )
    # todo: 認証機能を実装したら多分IsAuthenticatedに変更
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=utils.OpenApiRequest(
            serializers.PlayerSerializer,
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
                response=serializers.PlayerSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 201 response",
                        value={
                            "status": "ok",
                            "data": {
                                constants.PlayerFields.USER: {
                                    constants.UserFields.ID: 1,
                                    constants.UserFields.USERNAME: "username",
                                    constants.UserFields.EMAIL: "user@example.com",
                                },
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
        ) -> serializers.UserSerializer:
            # usernameのみBEがランダムな文字列をセット
            user_data[constants.UserFields.USERNAME] = (
                create_account.get_unique_random_username()
            )
            return serializers.UserSerializer(data=user_data)

        # サインアップ専用のUserSerializerを作成
        user_serializer: serializers.UserSerializer = _create_user_serializer(
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
            data={constants.PlayerFields.USER: user_serializer_data},
            status=status.HTTP_201_CREATED,
        )
