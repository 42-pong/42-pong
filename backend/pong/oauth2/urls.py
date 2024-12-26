from typing import Final

from django.urls import path

from .views import OAuth2AuthorizeView, OAuth2CallbackView

app_name: Final[str] = "oauth2"
urlpatterns = [
    # 'api/oauth2/'
    path("authorize/", OAuth2AuthorizeView.as_view(), name="oauth2_authorize"),
    path("callback/", OAuth2CallbackView.as_view(), name="oauth2_callback"),
]
