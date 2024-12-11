from django.urls import path

from .views import AccountCreateView

urlpatterns = [
    # api/accounts/
    path("", AccountCreateView.as_view(), name="accounts")
]
