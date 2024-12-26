from typing import Final

from django.urls import path

from . import views

app_name: Final[str] = "oauth2"
urlpatterns = [
    # 'api/oauth2/'
    path(
        "authorize/",
        views.OAuth2AuthorizeView.as_view(),
        name="authorize",
    ),
    path("callback/", views.OAuth2CallbackView.as_view(), name="callback"),
]
