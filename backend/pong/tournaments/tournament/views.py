from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiRequest,
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
                                },
                                {
                                    "id": 2,
                                    "status": "playing",
                                    "created_at": "2025-01-01T00:01:00.000000+09:00",
                                    "updated_at": "2025-01-01T00:02:00.000000+09:00",
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
                                "id": 1,
                                "status": "playing",
                                "created_at": "2025-01-01T00:00:00.000000+09:00",
                                "updated_at": "2025-01-01T00:30:00.000000+09:00",
                            },
                        },
                    ),
                ],
            ),
        },
    ),
    create=extend_schema(
        description="新しいTournamentレコードを作成する。",
        request=None,
        responses={
            201: OpenApiResponse(
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    OpenApiExample(
                        "example 201 response",
                        value={
                            "status": "ok",
                            "data": {
                                "id": 1,
                                "status": "matching",
                                "created_at": "2025-01-01t00:00:00.000000+09:00",
                                "updated_at": "2025-01-01t00:00:00.000000+09:00",
                            },
                        },
                    ),
                ],
            ),
        },
    ),
    partial_update=extend_schema(
        description="指定されたIDの大会情報の一部を更新します。",
        request=OpenApiRequest(
            request={"type": "object"},
            examples=[
                OpenApiExample(
                    "Example request",
                    value={
                        "status": "playing",
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
                                "status": "end",
                                "created_at": "2025-01-01T00:00:00.000000+09:00",
                                "updated_at": "2025-01-01T00:30:00.000000+09:00",
                            },
                        },
                    ),
                ],
            ),
        },
    ),
    destroy=extend_schema(
        description="指定されたIDのTournamentレコードを削除する。",
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
                                "status": "matching",
                                "created_at": "2025-01-01T00:00:00.000000+09:00",
                                "updated_at": "2025-01-01T00:00:00.000000+09:00",
                            },
                        },
                    ),
                ],
            ),
        },
    ),
)
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = models.Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer

    # 使用できるHTTPメソッドを制限
    http_method_names = ["get", "post", "patch", "delete"]
