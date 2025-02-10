from typing import Final

from django.urls import path

from .views import refresh, token

app_name: Final[str] = "tmp_jwt"
# todo: tmp_jwt完成後、simple-jwtを削除
urlpatterns = [
    # 'api/token/'
    path("", token.TokenObtainView.as_view(), name="token_obtain_pair"),
    path("refresh/", refresh.TokenRefreshView.as_view(), name="token_refresh"),
    # path("verify/", views.TokenVerifyView.as_view(), name="token_verify"),
]
