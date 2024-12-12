from django.urls import path

from .views import oauth_authorize, oauth_callback, oauth_fetch_token

urlpatterns = [
    # 'api/token/'
    path("authorize/", oauth_authorize, name="token_authorize"),
    path("callback/", oauth_callback, name="token_callback"),
    path("token/", oauth_fetch_token, name="token"),
]
