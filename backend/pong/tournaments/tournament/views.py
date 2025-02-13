from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets

from .. import constants
from . import models, serializers


@extend_schema_view(
    # requestやresponse, exampleは後で追記
    list=extend_schema(
        description="Tournamentレコード一覧を取得する。クエリパラメータによるフィルタリングも可能。",
        operation_id="tournaments_list",  # 明示的にoperationIdを設定
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
                name="status",
                description="トーナメントのステータス",
                required=False,
                type=str,
                enum=[
                    status.value
                    for status in constants.TournamentFields.StatusEnum
                ],
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
                                    "status": "end",
                                    "created_at": "2025-01-01T00:00:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:30:00.000000+09:00",
                                    "rounds": [
                                        {
                                            "round_number": 1,
                                            "status": "completed",
                                            "created_at": "2025-01-01T00:01:00.000000+09:00",
                                            "updated_at": "2025-01-01T00:10:00.000000+09:00",
                                            "matches": [
                                                {
                                                    "id": 1,
                                                    "round_id": 1,
                                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "player_id": 1,
                                                            "team": "1",
                                                            "created_at": "2025-02-11T14:00:46.920328+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:42.410054+09:00",
                                                                    "pos_x": 600,
                                                                    "pos_y": 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "player_id": 2,
                                                            "team": "2",
                                                            "created_at": "2025-02-11T14:01:01.839881+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:18.735550+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 100,
                                                                },
                                                                {
                                                                    "created_at": "2025-02-11T14:01:32.315450+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    "id": 2,
                                                    "round_id": 1,
                                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "player_id": 3,
                                                            "team": "1",
                                                            "created_at": "2025-02-11T14:00:46.920328+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:42.410054+09:00",
                                                                    "pos_x": 600,
                                                                    "pos_y": 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "player_id": 4,
                                                            "team": "2",
                                                            "created_at": "2025-02-11T14:01:01.839881+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:18.735550+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 100,
                                                                },
                                                                {
                                                                    "created_at": "2025-02-11T14:01:32.315450+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                        {
                                            "round_number": 2,
                                            "status": "completed",
                                            "created_at": "2025-01-01T00:01:00.000000+09:00",
                                            "updated_at": "2025-01-01T00:10:00.000000+09:00",
                                            "matches": [
                                                {
                                                    "id": 3,
                                                    "round_id": 2,
                                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "player_id": 2,
                                                            "team": "1",
                                                            "created_at": "2025-02-11T14:00:46.920328+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:42.410054+09:00",
                                                                    "pos_x": 600,
                                                                    "pos_y": 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "player_id": 3,
                                                            "team": "2",
                                                            "created_at": "2025-02-11T14:01:01.839881+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:18.735550+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 100,
                                                                },
                                                                {
                                                                    "created_at": "2025-02-11T14:01:32.315450+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                }
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "id": 2,
                                    "status": "matching",
                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:02:00.000000+09:00",
                                    "rounds": [{}],
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
        description="指定されたIDのTournamentレコードの詳細を取得する。",
        operation_id="tournaments_retrieve_by_id",  # 明示的にoperationIdを設定
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
                                    "status": "end",
                                    "created_at": "2025-01-01T00:00:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:30:00.000000+09:00",
                                    "rounds": [
                                        {
                                            "round_number": 1,
                                            "status": "completed",
                                            "created_at": "2025-01-01T00:01:00.000000+09:00",
                                            "updated_at": "2025-01-01T00:10:00.000000+09:00",
                                            "matches": [
                                                {
                                                    "id": 1,
                                                    "round_id": 1,
                                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "player_id": 1,
                                                            "team": "1",
                                                            "created_at": "2025-02-11T14:00:46.920328+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:42.410054+09:00",
                                                                    "pos_x": 600,
                                                                    "pos_y": 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "player_id": 2,
                                                            "team": "2",
                                                            "created_at": "2025-02-11T14:01:01.839881+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:18.735550+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 100,
                                                                },
                                                                {
                                                                    "created_at": "2025-02-11T14:01:32.315450+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    "id": 2,
                                                    "round_id": 1,
                                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "player_id": 3,
                                                            "team": "1",
                                                            "created_at": "2025-02-11T14:00:46.920328+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:42.410054+09:00",
                                                                    "pos_x": 600,
                                                                    "pos_y": 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "player_id": 4,
                                                            "team": "2",
                                                            "created_at": "2025-02-11T14:01:01.839881+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:18.735550+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 100,
                                                                },
                                                                {
                                                                    "created_at": "2025-02-11T14:01:32.315450+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                        {
                                            "round_number": 2,
                                            "status": "completed",
                                            "created_at": "2025-01-01T00:01:00.000000+09:00",
                                            "updated_at": "2025-01-01T00:10:00.000000+09:00",
                                            "matches": [
                                                {
                                                    "id": 3,
                                                    "round_id": 2,
                                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "player_id": 2,
                                                            "team": "1",
                                                            "created_at": "2025-02-11T14:00:46.920328+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:42.410054+09:00",
                                                                    "pos_x": 600,
                                                                    "pos_y": 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "player_id": 3,
                                                            "team": "2",
                                                            "created_at": "2025-02-11T14:01:01.839881+09:00",
                                                            "scores": [
                                                                {
                                                                    "created_at": "2025-02-11T14:01:18.735550+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 100,
                                                                },
                                                                {
                                                                    "created_at": "2025-02-11T14:01:32.315450+09:00",
                                                                    "pos_x": 0,
                                                                    "pos_y": 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                }
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ),
                ],
            ),
        },
    ),
)
class TournamentReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tournament.objects.all().prefetch_related(
        "rounds__matches__match_participations__scores"
    )
    serializer_class = serializers.TournamentSerializer
