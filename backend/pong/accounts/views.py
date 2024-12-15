from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status

# todo: IsAuthenticatedが追加されたらAllowAnyは不要かも
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import PlayerFields, UserFields
from .models import Player
from .serializers import PlayerSerializer


class AccountCreateView(APIView):
    serializer_class: type[PlayerSerializer] = PlayerSerializer
    # todo: 認証機能を実装したら多分IsAuthenticatedに変更
    permission_classes = (AllowAny,)

    @extend_schema(
        request=OpenApiRequest(
            PlayerSerializer,
            examples=[
                OpenApiExample(
                    "Example request",
                    value={
                        PlayerFields.USER: {
                            UserFields.USERNAME: "username",
                            UserFields.EMAIL: "user@example.com",
                            UserFields.PASSWORD: "password",
                        }
                    },
                ),
            ],
        ),
        responses={
            201: OpenApiResponse(
                response=PlayerSerializer,
                examples=[
                    OpenApiExample(
                        "Example 201 response",
                        value={
                            "player_id": 1,  # todo: Player,UserどちらのIDを返すか決めて変更
                            UserFields.USERNAME: "username",
                            UserFields.EMAIL: "user@example.com",
                        },
                    ),
                ],
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                    },
                },
                examples=[
                    OpenApiExample(
                        "Example 400 response",
                        value={"field": "error messages"},
                    ),
                ],
            ),
        },
    )
    # todo: try-exceptを書いて予期せぬエラー(実装上のミスを含む)の場合に500を返す
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        # requestをserializerに渡して変換とバリデーションを行う
        player_serializer = self.serializer_class(data=request.data)
        if not player_serializer.is_valid():
            return Response(
                player_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Account(PlayerとUser)を新規作成してDBに追加し、作成された情報を返す
        player: Player = player_serializer.save()
        return Response(
            {
                "player_id": player.id,  # todo: Player,UserどちらのIDを返すか決めて変更
                UserFields.USERNAME: player.user.username,
                UserFields.EMAIL: player.user.email,
            },
            status=status.HTTP_201_CREATED,
        )
