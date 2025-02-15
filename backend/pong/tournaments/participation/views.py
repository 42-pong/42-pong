from django.db.models import QuerySet
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, viewsets

from accounts.player import models as player_models
from pong import readonly_custom_renderer

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
                                    "tournament_id": 4,
                                    "user_id": 7,
                                    "participation_name": "player_x",
                                    "ranking": 4,
                                    "created_at": "2025-01-01T00:00:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:30:00.000000+09:00",
                                },
                                {
                                    "id": 2,
                                    "tournament_id": 5,
                                    "user_id": 7,
                                    "participation_name": "player_y",
                                    "ranking": None,
                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:01:00.000000+09:00",
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
)
class ParticipationReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ParticipationSerializer
    renderer_classes = [readonly_custom_renderer.ReadOnlyCustomJSONRenderer]

    def get_queryset(self) -> QuerySet:
        queryset = models.Participation.objects.all()
        user_id = self.request.query_params.get("user-id")
        tournament_id = self.request.query_params.get("tournament-id")

        if user_id:
            # 例外を出すと面倒なのでfilterとfirstを使っている
            player = player_models.Player.objects.filter(
                user_id=user_id
            ).first()
            if player:
                queryset = queryset.filter(player_id=player.id)
            else:
                queryset = (
                    queryset.none()
                )  # プレイヤーが見つからなければ空のクエリセットを返す

        if tournament_id:
            queryset = queryset.filter(tournament_id=tournament_id)

        return queryset
