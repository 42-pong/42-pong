from django.urls import path

from .views import oauth2_authorize, oauth2_callback

urlpatterns = [
    # 'api/oauth2/'
    path("authorize/", oauth2_authorize, name="oauth2_authorize"),
    path("callback/", oauth2_callback, name="oauth2_callback"),
]
