from django.urls import path
from .views import oauth_authorize, oauth_callback, oauth_fetch_token

urlpatterns = [
    # 'api/token/'
    path("authorize/", oauth_authorize, name="token_obtain_pair"),
    path("callback/", oauth_callback, name="token_refresh"),
    path("token/", oauth_fetch_token, name="token"),
]
