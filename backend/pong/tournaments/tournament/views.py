from typing import Optional

from django.db.models import Q, QuerySet
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, viewsets

from matches import constants as matches_constants
from pong import readonly_custom_renderer
from pong.custom_response import custom_response

from .. import constants as tournaments_constants
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
                    for status in tournaments_constants.TournamentFields.StatusEnum
                ],
                location=OpenApiParameter.QUERY,
            ),
        ],
        request=None,
        responses={
            200: OpenApiResponse(
                response=serializers.TournamentSerializer,
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: [
                                {
                                    tournaments_constants.TournamentFields.ID: 1,
                                    tournaments_constants.TournamentFields.STATUS: tournaments_constants.TournamentFields.StatusEnum.COMPLETED.value,
                                    tournaments_constants.TournamentFields.CREATED_AT: "2025-01-01T00:00:00.000000+09:00",
                                    tournaments_constants.TournamentFields.UPDATED_AT: "2025-01-01T00:30:00.000000+09:00",
                                    "rounds": [
                                        {
                                            tournaments_constants.RoundFields.ROUND_NUMBER: 1,
                                            tournaments_constants.RoundFields.STATUS: tournaments_constants.RoundFields.StatusEnum.COMPLETED.value,
                                            tournaments_constants.RoundFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                            tournaments_constants.RoundFields.UPDATED_AT: "2025-01-01T00:10:00.000000+09:00",
                                            "matches": [
                                                {
                                                    matches_constants.MatchFields.ID: 1,
                                                    matches_constants.MatchFields.ROUND_ID: 1,
                                                    matches_constants.MatchFields.STATUS: matches_constants.MatchFields.StatusEnum.COMPLETED.value,
                                                    matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    matches_constants.MatchFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "user_id": 1,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                            matches_constants.ParticipationFields.IS_WIN: True,
                                                            "scores": [
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:42.410054+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 600,
                                                                    matches_constants.ScoreFields.POS_Y: 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "user_id": 2,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                            matches_constants.ParticipationFields.IS_WIN: False,
                                                            "scores": [
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:18.735550+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 0,
                                                                    matches_constants.ScoreFields.POS_Y: 100,
                                                                },
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:32.315450+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 0,
                                                                    matches_constants.ScoreFields.POS_Y: 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    matches_constants.MatchFields.ID: 2,
                                                    matches_constants.MatchFields.ROUND_ID: 1,
                                                    matches_constants.MatchFields.STATUS: matches_constants.MatchFields.StatusEnum.COMPLETED.value,
                                                    matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    matches_constants.MatchFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "user_id": 3,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                            matches_constants.ParticipationFields.IS_WIN: False,
                                                            "scores": [
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:32.315450+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 600,
                                                                    matches_constants.ScoreFields.POS_Y: 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "user_id": 4,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                            matches_constants.ParticipationFields.IS_WIN: True,
                                                            "scores": [
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:18.735550+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 0,
                                                                    matches_constants.ScoreFields.POS_Y: 100,
                                                                },
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:32.315450+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 0,
                                                                    matches_constants.ScoreFields.POS_Y: 380,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                        {
                                            tournaments_constants.RoundFields.ROUND_NUMBER: 2,
                                            tournaments_constants.RoundFields.STATUS: tournaments_constants.RoundFields.StatusEnum.COMPLETED.value,
                                            tournaments_constants.RoundFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                            tournaments_constants.RoundFields.UPDATED_AT: "2025-01-01T00:10:00.000000+09:00",
                                            "matches": [
                                                {
                                                    matches_constants.MatchFields.ID: 3,
                                                    matches_constants.MatchFields.ROUND_ID: 2,
                                                    matches_constants.MatchFields.STATUS: matches_constants.MatchFields.StatusEnum.COMPLETED.value,
                                                    matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    matches_constants.MatchFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            "user_id": 2,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                            matches_constants.ParticipationFields.IS_WIN: True,
                                                            "scores": [
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-01-01T00:06:00.000000+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 600,
                                                                    matches_constants.ScoreFields.POS_Y: 10,
                                                                },
                                                                {"...", "..."},
                                                            ],
                                                        },
                                                        {
                                                            "user_id": 3,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                            matches_constants.ParticipationFields.IS_WIN: False,
                                                            "scores": [
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-01-01T00:06:10.000000+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 0,
                                                                    matches_constants.ScoreFields.POS_Y: 100,
                                                                },
                                                                {
                                                                    matches_constants.ScoreFields.CREATED_AT: "2025-01-01T00:06:20.000000+09:00",
                                                                    matches_constants.ScoreFields.POS_X: 0,
                                                                    matches_constants.ScoreFields.POS_Y: 380,
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
                                    tournaments_constants.TournamentFields.ID: 2,
                                    tournaments_constants.TournamentFields.STATUS: tournaments_constants.TournamentFields.StatusEnum.NOT_STARTED.value,
                                    tournaments_constants.TournamentFields.CREATED_AT: "2025-01-01T00:20:00.000000+09:00",
                                    tournaments_constants.TournamentFields.UPDATED_AT: "2025-01-01T00:40:00.000000+09:00",
                                    "rounds": [{}],
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
        description="指定されたIDのTournamentレコードの詳細を取得する。",
        operation_id="tournaments_retrieve_by_id",  # 明示的にoperationIdを設定
        responses={
            200: OpenApiResponse(
                response=serializers.TournamentSerializer,
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                tournaments_constants.TournamentFields.ID: 1,
                                tournaments_constants.TournamentFields.STATUS: tournaments_constants.TournamentFields.StatusEnum.COMPLETED.value,
                                tournaments_constants.TournamentFields.CREATED_AT: "2025-01-01T00:00:00.000000+09:00",
                                tournaments_constants.TournamentFields.UPDATED_AT: "2025-01-01T00:30:00.000000+09:00",
                                "rounds": [
                                    {
                                        tournaments_constants.RoundFields.ROUND_NUMBER: 1,
                                        tournaments_constants.RoundFields.STATUS: tournaments_constants.RoundFields.StatusEnum.COMPLETED.value,
                                        tournaments_constants.RoundFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                        tournaments_constants.RoundFields.UPDATED_AT: "2025-01-01T00:10:00.000000+09:00",
                                        "matches": [
                                            {
                                                matches_constants.MatchFields.ID: 1,
                                                matches_constants.MatchFields.ROUND_ID: 1,
                                                matches_constants.MatchFields.STATUS: matches_constants.MatchFields.StatusEnum.COMPLETED.value,
                                                matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                matches_constants.MatchFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                "participations": [
                                                    {
                                                        "user_id": 1,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                        matches_constants.ParticipationFields.IS_WIN: False,
                                                        "scores": [
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:42.410054+09:00",
                                                                matches_constants.ScoreFields.POS_X: 600,
                                                                matches_constants.ScoreFields.POS_Y: 10,
                                                            },
                                                            {"...", "..."},
                                                        ],
                                                    },
                                                    {
                                                        "user_id": 2,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                        matches_constants.ParticipationFields.IS_WIN: True,
                                                        "scores": [
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:18.735550+09:00",
                                                                matches_constants.ScoreFields.POS_X: 0,
                                                                matches_constants.ScoreFields.POS_Y: 100,
                                                            },
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:32.315450+09:00",
                                                                matches_constants.ScoreFields.POS_X: 0,
                                                                matches_constants.ScoreFields.POS_Y: 380,
                                                            },
                                                            {"...", "..."},
                                                        ],
                                                    },
                                                ],
                                            },
                                            {
                                                matches_constants.MatchFields.ID: 2,
                                                matches_constants.MatchFields.ROUND_ID: 1,
                                                matches_constants.MatchFields.STATUS: matches_constants.MatchFields.StatusEnum.COMPLETED.value,
                                                matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                matches_constants.MatchFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                "participations": [
                                                    {
                                                        "user_id": 3,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                        matches_constants.ParticipationFields.IS_WIN: True,
                                                        "scores": [
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:32.315450+09:00",
                                                                matches_constants.ScoreFields.POS_X: 600,
                                                                matches_constants.ScoreFields.POS_Y: 10,
                                                            },
                                                            {"...", "..."},
                                                        ],
                                                    },
                                                    {
                                                        "user_id": 4,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                        matches_constants.ParticipationFields.IS_WIN: False,
                                                        "scores": [
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:18.735550+09:00",
                                                                matches_constants.ScoreFields.POS_X: 0,
                                                                matches_constants.ScoreFields.POS_Y: 100,
                                                            },
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-02-11T14:01:32.315450+09:00",
                                                                matches_constants.ScoreFields.POS_X: 0,
                                                                matches_constants.ScoreFields.POS_Y: 380,
                                                            },
                                                            {"...", "..."},
                                                        ],
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    {
                                        tournaments_constants.RoundFields.ROUND_NUMBER: 2,
                                        tournaments_constants.RoundFields.STATUS: tournaments_constants.RoundFields.StatusEnum.COMPLETED.value,
                                        tournaments_constants.RoundFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                        tournaments_constants.RoundFields.UPDATED_AT: "2025-01-01T00:10:00.000000+09:00",
                                        "matches": [
                                            {
                                                matches_constants.MatchFields.ID: 3,
                                                matches_constants.MatchFields.ROUND_ID: 2,
                                                matches_constants.MatchFields.STATUS: matches_constants.MatchFields.StatusEnum.COMPLETED.value,
                                                matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                matches_constants.MatchFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                "participations": [
                                                    {
                                                        "user_id": 2,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                        matches_constants.ParticipationFields.IS_WIN: False,
                                                        "scores": [
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-01-01T00:06:00.000000+09:00",
                                                                matches_constants.ScoreFields.POS_X: 600,
                                                                matches_constants.ScoreFields.POS_Y: 10,
                                                            },
                                                            {"...", "..."},
                                                        ],
                                                    },
                                                    {
                                                        "user_id": 3,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                        matches_constants.ParticipationFields.IS_WIN: True,
                                                        "scores": [
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-01-01T00:06:10.000000+09:00",
                                                                matches_constants.ScoreFields.POS_X: 0,
                                                                matches_constants.ScoreFields.POS_Y: 100,
                                                            },
                                                            {
                                                                matches_constants.ScoreFields.CREATED_AT: "2025-01-01T00:06:20.000000+09:00",
                                                                matches_constants.ScoreFields.POS_X: 0,
                                                                matches_constants.ScoreFields.POS_Y: 380,
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
class TournamentReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TournamentSerializer
    renderer_classes = [readonly_custom_renderer.ReadOnlyCustomJSONRenderer]

    def get_queryset(self) -> QuerySet:
        queryset = models.Tournament.objects.all().prefetch_related(
            "round__matches__match_participations__scores"
        )

        filters = Q()

        status: Optional[str] = self.request.query_params.get("status")
        if status:
            filters &= Q(status=status)

        user_id: Optional[str] = self.request.query_params.get("user-id")
        if user_id:
            filters &= Q(tournament_participations__player__user_id=user_id)

        return queryset.filter(filters)
