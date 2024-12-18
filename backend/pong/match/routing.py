from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/match/", consumers.MultiEventConsumer.as_asgi())
]
