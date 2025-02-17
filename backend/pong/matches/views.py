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

from pong import readonly_custom_renderer
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
            OpenApiParameter(
                name="status",
                description="マッチのステータス",
                required=False,
                type=str,
                enum=[
                    status.value for status in constants.MatchFields.StatusEnum
                ],
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
                                    constants.MatchFields.STATUS: constants.MatchFields.StatusEnum.COMPLETED.value,
                                    constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                    constants.MatchFields.UPDATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                    "participations": [
                                        {
                                            constants.ParticipationFields.PLAYER_ID: 1,
                                            constants.ParticipationFields.TEAM: constants.ParticipationFields.TeamEnum.ONE.value,
                                            constants.ParticipationFields.IS_WIN: True,
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
                                            constants.ParticipationFields.IS_WIN: False,
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
                                    constants.MatchFields.STATUS: constants.MatchFields.StatusEnum.ON_GOING.value,
                                    constants.MatchFields.CREATED_AT: "2025-01-01T00:03:00.000000+09:00",
                                    constants.MatchFields.UPDATED_AT: "2025-01-01T00:06:00.000000+09:00",
                                    "participations": [{"..."}],
                                },
                                {
                                    constants.MatchFields.ID: 3,
                                    constants.MatchFields.ROUND_ID: 2,
                                    constants.MatchFields.STATUS: constants.MatchFields.StatusEnum.NOT_STARTED.value,
                                    constants.MatchFields.CREATED_AT: "2025-01-01T00:03:00.000000+09:00",
                                    constants.MatchFields.UPDATED_AT: "2025-01-01T00:06:00.000000+09:00",
                                    "participations": [{"..."}],
                                },
                                {"..."},
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
                                    constants.MatchFields.STATUS: constants.MatchFields.StatusEnum.COMPLETED.value,
                                    constants.MatchFields.CREATED_AT: "2025-01-01T00:01:00.000000+09:00",
                                    constants.MatchFields.UPDATED_AT: "2025-01-01T00:03:00.000000+09:00",
                                    "participations": [
                                        {
                                            constants.ParticipationFields.PLAYER_ID: 1,
                                            constants.ParticipationFields.TEAM: constants.ParticipationFields.TeamEnum.ONE.value,
                                            constants.ParticipationFields.IS_WIN: True,
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
                                            constants.ParticipationFields.IS_WIN: False,
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
                        custom_response.ERRORS: {"type": "string"},
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
class MatchReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.MatchSerializer
    renderer_classes = [readonly_custom_renderer.ReadOnlyCustomJSONRenderer]

    def get_queryset(self) -> QuerySet:
        queryset = match_models.Match.objects.all().prefetch_related(
            "match_participations__scores"
        )

        filters = Q()

        status: Optional[str] = self.request.query_params.get("status")
        if status:
            filters &= Q(status=status)

        user_id: Optional[str] = self.request.query_params.get("user-id")
        if user_id:
            filters &= Q(match_participations__player__user_id=user_id)

        return queryset.filter(filters)
