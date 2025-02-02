from typing import Final

from django.urls import path

from .views import list, retrieve

app_name: Final[str] = "users"
urlpatterns = [
    # api/users/
    path("", list.UsersListView.as_view(), name="list"),
    path(
        "<int:user_id>/",
        retrieve.UsersRetrieveView.as_view(),
        name="retrieve",
    ),
]
