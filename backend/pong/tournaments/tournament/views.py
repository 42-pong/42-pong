from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets

from matches import constants as matches_constants

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
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": [
                                {
                                    tournaments_constants.TournamentFields.ID: 1,
                                    tournaments_constants.TournamentFields.STATUS: tournaments_constants.TournamentFields.StatusEnum.END.value,
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
                                                    matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            matches_constants.ParticipationFields.PLAYER_ID: 1,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                            matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:00:46.920328+09:00",
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
                                                            matches_constants.ParticipationFields.PLAYER_ID: 2,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                            matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:01:01.839881+09:00",
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
                                                    matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            matches_constants.ParticipationFields.PLAYER_ID: 3,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                            matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:00:46.920328+09:00",
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
                                                            matches_constants.ParticipationFields.PLAYER_ID: 4,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                            matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:01:01.839881+09:00",
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
                                                    matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:05:00.000000+09:00",
                                                    "participations": [
                                                        {
                                                            matches_constants.ParticipationFields.PLAYER_ID: 2,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                            matches_constants.ParticipationFields.CREATED_AT: "2025-01-01T00:05:10.000000+09:00",
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
                                                            matches_constants.ParticipationFields.PLAYER_ID: 3,
                                                            matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                            matches_constants.ParticipationFields.CREATED_AT: "2025-01-01T00:05:10.000000+09:00",
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
                                    tournaments_constants.TournamentFields.STATUS: tournaments_constants.TournamentFields.StatusEnum.MATCHING.value,
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
                            "data": {
                                tournaments_constants.TournamentFields.ID: 1,
                                tournaments_constants.TournamentFields.STATUS: tournaments_constants.TournamentFields.StatusEnum.END.value,
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
                                                matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                "participations": [
                                                    {
                                                        matches_constants.ParticipationFields.PLAYER_ID: 1,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                        matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:00:46.920328+09:00",
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
                                                        matches_constants.ParticipationFields.PLAYER_ID: 2,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                        matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:01:01.839881+09:00",
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
                                                matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                                "participations": [
                                                    {
                                                        matches_constants.ParticipationFields.PLAYER_ID: 3,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                        matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:00:46.920328+09:00",
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
                                                        matches_constants.ParticipationFields.PLAYER_ID: 4,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                        matches_constants.ParticipationFields.CREATED_AT: "2025-02-11T14:01:01.839881+09:00",
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
                                                matches_constants.MatchFields.CREATED_AT: "2025-01-01T00:05:00.000000+09:00",
                                                "participations": [
                                                    {
                                                        matches_constants.ParticipationFields.PLAYER_ID: 2,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.ONE.value,
                                                        matches_constants.ParticipationFields.CREATED_AT: "2025-01-01T00:05:10.000000+09:00",
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
                                                        matches_constants.ParticipationFields.PLAYER_ID: 3,
                                                        matches_constants.ParticipationFields.TEAM: matches_constants.ParticipationFields.TeamEnum.TWO.value,
                                                        matches_constants.ParticipationFields.CREATED_AT: "2025-01-01T00:05:10.000000+09:00",
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
        },
    ),
)
class TournamentReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tournament.objects.all().prefetch_related(
        "round__matches__match_participations__scores"
    )
    serializer_class = serializers.TournamentSerializer
