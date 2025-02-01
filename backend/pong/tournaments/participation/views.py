from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets

from . import models, serializers


@extend_schema_view(
    # requestやresponse, exampleは後で追記
    list=extend_schema(
        description="Participationレコード一覧を取得する。クエリパラメータによるフィルタリングも可能。",
        operation_id="participations_list",  # 明示的にoperationIdを設定
        parameters=[
            OpenApiParameter(
                # 実際には、user_idからplayer_idを取得してフィルタリングする。
                name="user-id",
                description="userテーブルのID",
                required=False,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="tournament-id",
                description="TournamentテーブルのID",
                required=False,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        request=None,
        responses={
            200: OpenApiResponse(
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": [
                                {
                                    "id": 1,
                                    "participation_name": "player_x",
                                    "ranking": 4,
                                    "created_at": "2025-01-01T00:00:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:30:00.000000+09:00",
                                    "tournament_id": 4,
                                    "user_id": 7,
                                },
                                {
                                    "id": 2,
                                    "participation_name": "player_y",
                                    "ranking": None,
                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:01:00.000000+09:00",
                                    "tournament_id": 5,
                                    "user_id": 7,
                                },
                                {"...", "..."},
                            ],
                        },
                    ),
                ],
            ),
        },
    ),
    retrieve=extend_schema(
        description="指定されたIDのParticipationレコードの詳細を取得する。",
        operation_id="participations_retrieve_by_id",  # 明示的にoperationIdを設定
        responses={
            200: OpenApiResponse(
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": {
                                "id": 1,
                                "participation_name": "player_x",
                                "ranking": 1,
                                "created_at": "2025-01-01T00:00:00.000000+09:00",
                                "updated_at": "2025-01-01T00:30:00.000000+09:00",
                                "tournament_id": 2,
                                "user_id": 3,
                            },
                        },
                    ),
                ],
            ),
        },
    ),
    create=extend_schema(
        description="新しいParticipationレコードを作成する。",
        request=OpenApiRequest(
            request={"type": "object"},
            examples=[
                OpenApiExample(
                    "Example request",
                    value={
                        "tournament_id": 1,
                        "player_id": 2,
                        "participation_name": "player_x",
                    },
                ),
            ],
        ),
        responses={
            201: OpenApiResponse(
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 201 response",
                        value={
                            "status": "ok",
                            "data": {
                                "id": 1,
                                "participation_name": "player_x",
                                "ranking": None,
                                "created_at": "2025-01-01T00:00:00.000000+09:00",
                                "updated_at": "2025-01-01T00:00:00.000000+09:00",
                                "tournament_id": 2,
                                "user_id": 3,
                            },
                        },
                    ),
                ],
            ),
        },
    ),
    partial_update=extend_schema(
        description="指定されたIDのParticipationレコードのランキングを登録します。",
        request=OpenApiRequest(
            request={"type": "object"},
            examples=[
                OpenApiExample(
                    "Example request",
                    value={
                        "ranking": 1,
                    },
                ),
            ],
        ),
        responses={
            200: OpenApiResponse(
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": {
                                "id": 1,
                                "participation_name": "player_x",
                                "ranking": 1,
                                "created_at": "2025-01-01T00:00:00.000000+09:00",
                                "updated_at": "2025-01-01T00:30:00.000000+09:00",
                                "tournament_id": 2,
                                "user_id": 3,
                            },
                        },
                    ),
                ],
            ),
        },
    ),
    destroy=extend_schema(
        description="指定されたIDのParticipationレコードを削除する。",
        responses={
            204: OpenApiResponse(
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 204 response",
                        value={
                            "status": "ok",
                            "data": {
                                "id": 1,
                                "participation_name": "player_x",
                                "ranking": 1,
                                "created_at": "2025-01-01T00:00:00.000000+09:00",
                                "updated_at": "2025-01-01T00:30:00.000000+09:00",
                                "tournament_id": 2,
                                "user_id": 3,
                            },
                        },
                    ),
                ],
            ),
        },
    ),
)
class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = models.Participation.objects.all()
    serializer_class = serializers.ParticipationSerializer

    # 使用できるHTTPメソッドを制限
    http_method_names = ["get", "post", "patch", "delete"]
