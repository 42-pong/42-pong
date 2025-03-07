from typing import Final

from django.urls import path

from .views import login, totp

app_name: Final[str] = "login"
urlpatterns = [
    # 'api/token/'
    path("", login.LoginView.as_view(), name="login"),
    path("/totp", totp.TotpView.as_view(), name="totp"),
]
