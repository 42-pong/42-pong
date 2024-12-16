"""
ASGI config for pong project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
import match.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pong.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator( # settings.pyのALLOWED_HOSTの設定を適用
            # Djangoのセッション管理は使用しないので,AuthMiddlewareStackは使用しない
            # TODO: JWTAuthMiddlewareを作成して使用する
            URLRouter(
                routing.websocket_urlpatterns
            ),
        ),
    }
)
