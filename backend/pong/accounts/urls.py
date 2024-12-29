from typing import Final

from django.urls import path

from . import views

app_name: Final[str] = "accounts"
urlpatterns = [
    # api/accounts/
    path("", views.AccountCreateView.as_view(), name="account_create")
]
