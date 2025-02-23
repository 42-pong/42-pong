from django.urls import path

from ws.tournament import manager_registry

from . import consumers

# グローバルな'TournamentManagerRegistry'を作成
tournament_manager_registry = manager_registry.TournamentManagerRegistry()

websocket_urlpatterns = [
    path(
        "ws/",
        consumers.MultiEventConsumer.as_asgi(),
        # consumerがself.scopeでTournamentManagerRegistryを受け取るために必要
        {"tournament_manager_registry": tournament_manager_registry},
    )
]
