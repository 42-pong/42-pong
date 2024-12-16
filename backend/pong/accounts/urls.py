from typing import Final

from django.urls import path

from .views import AccountCreateView

app_name: Final[str] = "accounts"
urlpatterns = [
    # api/accounts/
    path("", AccountCreateView.as_view(), name="accounts")
]
