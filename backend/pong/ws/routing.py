from django.urls import path

#from ws.tournament import manager_registry

from . import consumers

websocket_urlpatterns = [
    path(
        "ws/",
        consumers.MultiEventConsumer.as_asgi(),
    )
]
