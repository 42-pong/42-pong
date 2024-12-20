from django.urls import path

from .views import OAuth2AuthorizeView, OAuth2CallbackView

urlpatterns = [
    # 'api/oauth2/'
    path("authorize/", OAuth2AuthorizeView.as_view(), name="oauth2_authorize"),
    path("callback/", OAuth2CallbackView.as_view(), name="oauth2_callback"),
]
