from typing import Final

from django.urls import path
from rest_framework_simplejwt import views

app_name: Final[str] = "tmp_jwt"
urlpatterns = [
    # 'api/token/'
    path("", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", views.TokenVerifyView.as_view(), name="token_verify"),
]
