from typing import Final

from django.urls import path

from . import views
from .views import verify_otp

app_name: Final[str] = "accounts"
urlpatterns = [
    # api/accounts/
    path("", views.AccountCreateView.as_view(), name="account_create"),
    path("otp/verify/", verify_otp.VerifyOTPView.as_view(), name="verify_otp"),
]
