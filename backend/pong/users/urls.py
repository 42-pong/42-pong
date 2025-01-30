from typing import Final

from django.urls import path

from .views import list

app_name: Final[str] = "users"
urlpatterns = [
    # api/users/
    path("", list.UsersListView.as_view(), name="list"),
]
