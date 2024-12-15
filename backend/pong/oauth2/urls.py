from django.urls import path

from .views import oauth2_authorize, oauth2_callback, oauth2_fetch_token

urlpatterns = [
    # 'api/oauth2/'
    path("authorize/", oauth2_authorize, name="oauth2_authorize"),
    path("callback/", oauth2_callback, name="oauth2_callback"),
    path("token/", oauth2_fetch_token, name="oauth2_fetch_token"),
]
