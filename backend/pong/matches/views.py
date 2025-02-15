from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, viewsets

from pong.custom_response import custom_response

from . import constants
from .match import models as match_models
from .match import serializers


@extend_schema_view(
    list=extend_schema(
        description="Match一覧を取得する。クエリパラメータによるフィルタリングも可能。",
        operation_id="matches_list",
        parameters=[
            OpenApiParameter(
                # 実際には、user_idからplayer_idを取得してフィルタリングする。
                name="user-id",
                description="userテーブルのID",
                required=False,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        request=None,
        responses={
            200: OpenApiResponse(
                description="A list of matches",
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: [
                                {
                                    constants.MatchFields.ID: 1,
                                    constants.MatchFields.ROUND_ID: 1,
                                    "participations": [
                                        {
                                            constants.ParticipationFields.PLAYER_ID: 1,
                                            constants.ParticipationFields.TEAM: constants.ParticipationFields.TeamEnum.ONE.value,
                                            "scores": [
                                                {
                                                    constants.ScoreFields.CREATED_AT: "2025-01-01T00:00:00.000000+09:00",
                                                    constants.ScoreFields.POS_X: 600,
                                                    constants.ScoreFields.POS_Y: 10,
                                                },
                                                {"..."},
                                            ],
                                        },
                                        {
                                            constants.ParticipationFields.PLAYER_ID: 2,
                                            constants.ParticipationFields.TEAM: constants.ParticipationFields.TeamEnum.TWO.value,
                                            "scores": [
                                                {
                                                    constants.ScoreFields.CREATED_AT: "2025-01-01T00:00:30.000000+09:00",
                                                    constants.ScoreFields.POS_X: 0,
                                                    constants.ScoreFields.POS_Y: 380,
                                                },
                                                {"..."},
                                            ],
                                        },
                                    ],
                                },
                                {
                                    constants.MatchFields.ID: 2,
                                    constants.MatchFields.ROUND_ID: 1,
                                    "participations": [{"..."}],
                                },
                                {
                                    constants.MatchFields.ID: 3,
                                    constants.MatchFields.ROUND_ID: 2,
                                    "participations": [{"..."}],
                                },
                                {"..."},
                            ],
                        },
                    ),
                ],
            ),
            # todo: 詳細のschemaが必要であれば追加する
            500: OpenApiResponse(description="Internal server error"),
        },
    ),
    retrieve=extend_schema(
        description="特定のMatchを取得する。",
        operation_id="matches_retrieve_by_id",
        request=None,
        responses={
            200: OpenApiResponse(
                description="A detail of a match",
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: [
                                {
                                    constants.MatchFields.ID: 1,
                                    constants.MatchFields.ROUND_ID: 1,
                                    "participations": [
                                        {
                                            constants.ParticipationFields.PLAYER_ID: 1,
                                            constants.ParticipationFields.TEAM: constants.ParticipationFields.TeamEnum.ONE.value,
                                            "scores": [
                                                {
                                                    constants.ScoreFields.CREATED_AT: "2025-01-01T00:00:00.000000+09:00",
                                                    constants.ScoreFields.POS_X: 600,
                                                    constants.ScoreFields.POS_Y: 10,
                                                },
                                                {"..."},
                                            ],
                                        },
                                        {
                                            constants.ParticipationFields.PLAYER_ID: 2,
                                            constants.ParticipationFields.TEAM: constants.ParticipationFields.TeamEnum.TWO.value,
                                            "scores": [
                                                {
                                                    constants.ScoreFields.CREATED_AT: "2025-01-01T00:00:30.000000+09:00",
                                                    constants.ScoreFields.POS_X: 0,
                                                    constants.ScoreFields.POS_Y: 380,
                                                },
                                                {"..."},
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ),
                ],
            ),
            # todo: 詳細のschemaが必要であれば追加する
            500: OpenApiResponse(description="Internal server error"),
        },
    ),
)
class MatchReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = match_models.Match.objects.all().prefetch_related(
        "match_participations__scores"
    )
    serializer_class = serializers.MatchSerializer
