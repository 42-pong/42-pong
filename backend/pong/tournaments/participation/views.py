from typing import Optional

import rest_framework_simplejwt
from django.db.models import Q, QuerySet
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, viewsets

from pong import readonly_custom_renderer
from pong.custom_response import custom_response

from .. import constants
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
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: [
                                {
                                    constants.ParticipationFields.ID: 1,
                                    constants.ParticipationFields.TOURNAMENT_ID: 4,
                                    "user_id": 7,
                                    constants.ParticipationFields.PARTICIPATION_NAME: "player_x",
                                    constants.ParticipationFields.RANKING: 4,
                                    constants.ParticipationFields.CREATED_AT: "2025-01-01T00:00:00.000000+09:00",
                                    constants.ParticipationFields.UPDATED_AT: "2025-01-01T00:30:00.000000+09:00",
                                },
                                {
                                    constants.ParticipationFields.ID: 2,
                                    constants.ParticipationFields.TOURNAMENT_ID: 5,
                                    "user_id": 7,
                                    constants.ParticipationFields.PARTICIPATION_NAME: "player_y",
                                    constants.ParticipationFields.RANKING: None,
                                    constants.ParticipationFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                    constants.ParticipationFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                },
                                {"...", "..."},
                            ],
                        },
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Not authenticated",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    OpenApiExample(
                        "Example 401 response",
                        value={
                            "detail": "Authentication credentials were not provided."
                        },
                    ),
                ],
            ),
            # todo: 詳細のschemaが必要であれば追加する
            500: OpenApiResponse(description="Internal server error"),
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
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                constants.ParticipationFields.ID: 4,
                                constants.ParticipationFields.TOURNAMENT_ID: 2,
                                "user_id": 3,
                                constants.ParticipationFields.PARTICIPATION_NAME: "player_x",
                                constants.ParticipationFields.RANKING: 1,
                                constants.ParticipationFields.CREATED_AT: "2025-01-01T00:15:00.000000+09:00",
                                constants.ParticipationFields.UPDATED_AT: "2025-01-01T00:20:00.000000+09:00",
                            },
                        },
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Not authenticated",
                response={
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                },
                examples=[
                    OpenApiExample(
                        "Example 401 response",
                        value={
                            "detail": "Authentication credentials were not provided."
                        },
                    ),
                ],
            ),
            404: OpenApiResponse(
                description="Not Found",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.CODE: {"type": "list"},
                        custom_response.ERRORS: {"type": "dict"},
                    },
                },
                examples=[
                    OpenApiExample(
                        "Example 404 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                custom_response.Code.INTERNAL_ERROR
                            ],
                            custom_response.ERRORS: {
                                "id": "The resource does not exist."
                            },
                        },
                    ),
                ],
            ),
            # todo: 詳細のschemaが必要であれば追加する
            500: OpenApiResponse(description="Internal server error"),
        },
    ),
)
class ParticipationReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    # todo: 自作JWTの認証クラスを設定する
    authentication_classes = [
        rest_framework_simplejwt.authentication.JWTAuthentication
    ]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ParticipationQuerySerializer
    renderer_classes = [readonly_custom_renderer.ReadOnlyCustomJSONRenderer]

    def get_queryset(self) -> QuerySet:
        queryset = models.Participation.objects.all()
        filters = Q()

        user_id: Optional[str] = self.request.query_params.get("user-id")
        if user_id is not None:
            filters &= Q(
                player__user_id=user_id
            )  # 直接関連をたどってフィルタリング

        tournament_id: Optional[str] = self.request.query_params.get(
            "tournament-id"
        )
        if tournament_id is not None:
            filters &= Q(tournament_id=tournament_id)

        return queryset.filter(filters)
