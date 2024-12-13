from django.urls import path

from .views import oauth2_authorize, oauth2_callback, oauth2_fetch_token

urlpatterns = [
    # 'api/token/'
    path("authorize/", oauth2_authorize, name="token_authorize"),
    path("callback/", oauth2_callback, name="token_callback"),
    path("token/", oauth2_fetch_token, name="token"),
]
