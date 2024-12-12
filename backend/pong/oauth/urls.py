from django.urls import path
from .views import oauth_authorize

urlpatterns = [
    # 'api/token/'
    path("authorize/", oauth_authorize, name="token_obtain_pair"),
]
