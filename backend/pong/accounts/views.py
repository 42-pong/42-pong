from django.contrib.auth.models import User
from drf_spectacular import utils

# todo: IsAuthenticatedが追加されたらAllowAnyは不要かも
from rest_framework import permissions, request, response, status, views

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
                            constants.PlayerFields.USER: {
                                constants.UserFields.ID: 1,
                                constants.UserFields.USERNAME: "username",
                                constants.UserFields.EMAIL: "user@example.com",
                            }
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "error": {"type": ["string"]},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response",
                        value={"error": {"field": ["error messages"]}},
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
        # todo: pop()する前にrequestのfieldのvalidationが必要かも

        # サインアップ専用のUserSerializerを作成
        user_data: dict = request.data.pop(constants.PlayerFields.USER)
        # usernameのみBEがランダムな文字列をセット
        user_data[constants.UserFields.USERNAME] = (
            create_account.get_unique_random_username()
        )
        user_serializer: serializers.UserSerializer = (
            serializers.UserSerializer(data=user_data)
        )
        if not user_serializer.is_valid():
            return response.Response(
                {"error": user_serializer.errors},
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
            return response.Response(
                {"error": create_account_result.unwrap_error()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user: User = create_account_result.unwrap()
        return response.Response(
            {
                constants.PlayerFields.USER: {
                    constants.UserFields.ID: user.id,
                    constants.UserFields.USERNAME: user.username,
                    constants.UserFields.EMAIL: user.email,
                }
            },
            status=status.HTTP_201_CREATED,
        )
