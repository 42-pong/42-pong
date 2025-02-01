from typing import Final

from django.urls import path

from . import views

app_name: Final[str] = "users"
urlpatterns = [
    # api/users/
    path("", views.UsersListView.as_view(), name="users_list"),
]
