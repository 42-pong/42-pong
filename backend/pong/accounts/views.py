from drf_spectacular import utils

# todo: IsAuthenticatedが追加されたらAllowAnyは不要かも
from rest_framework import permissions, request, response, status, views

from . import constants, models, serializers


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
                            constants.UserFields.USERNAME: "username",
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
                        "error": {"type": "string"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response",
                        value={"field": "error messages"},
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
        requestをPlayerSerializerに渡してvalidationを行い、
        有効な場合はPlayerとUserを作成してDBに追加し、作成されたアカウント情報をresponseとして返す
        """
        # requestをserializerに渡して変換とバリデーションを行う
        player_serializer: serializers.PlayerSerializer = (
            self.serializer_class(data=request.data)
        )
        if not player_serializer.is_valid():
            return response.Response(
                player_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Account(PlayerとUser)を新規作成してDBに追加し、作成された情報を返す
        player: models.Player = player_serializer.save()
        return response.Response(
            {
                constants.PlayerFields.USER: {
                    constants.UserFields.ID: player.user.id,
                    constants.UserFields.USERNAME: player.user.username,
                    constants.UserFields.EMAIL: player.user.email,
                }
            },
            status=status.HTTP_201_CREATED,
        )
