from django.urls import path

from . import views

urlpatterns = [
    # api/accounts/
    path("", views.AccountCreateView.as_view(), name="accounts")
]
