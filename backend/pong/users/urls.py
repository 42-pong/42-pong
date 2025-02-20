from typing import Final

from django.urls import include, path

from .views import list, me, retrieve

app_name: Final[str] = "users"
urlpatterns = [
    # api/users/
    path("", list.UsersListView.as_view(), name="list"),
    path(
        "<int:user_id>/", retrieve.UsersRetrieveView.as_view(), name="retrieve"
    ),
    path("me/", me.UsersMeView.as_view(), name="me"),
    path("me/friends/", include("users.friends.urls", namespace="friends")),
    path("me/blocks/", include("users.blocks.urls", namespace="blocks")),
]
