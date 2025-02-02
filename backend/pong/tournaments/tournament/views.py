from drf_spectacular.utils import (
    OpenApiParameter,
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
    ),
    retrieve=extend_schema(
        description="指定されたIDのTournamentレコードの詳細を取得する。",
        operation_id="tournaments_retrieve_by_id",  # 明示的にoperationIdを設定
    ),
    create=extend_schema(
        description="新しいTournamentレコードを作成する。",
    ),
    partial_update=extend_schema(
        description="指定されたIDの大会情報の一部を更新します。",
    ),
    destroy=extend_schema(
        description="指定されたIDのTournamentレコードを削除する。",
    ),
)
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = models.Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer

    # 使用できるHTTPメソッドを制限
    http_method_names = ["get", "post", "patch", "delete"]
