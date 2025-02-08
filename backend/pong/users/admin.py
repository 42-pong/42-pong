from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .friends import constants, models


@admin.register(models.Friendship)
class FriendshipAdmin(ModelAdmin):
    list_display: tuple = (
        constants.FriendshipFields.ID,
        constants.FriendshipFields.USER_ID,
        "username",
        constants.FriendshipFields.FRIEND_USER_ID,
        "friend_username",
        constants.FriendshipFields.CREATED_AT,
        constants.FriendshipFields.UPDATED_AT,
    )
    search_fields: tuple = (
        "user__id",
        "user__username",
        "friend__id",
        "friend__username",
    )
    list_filter: tuple = (
        "user__id",
        constants.FriendshipFields.CREATED_AT,
        constants.FriendshipFields.UPDATED_AT,
    )
    ordering: tuple = (f"-{constants.FriendshipFields.CREATED_AT}",)

    def username(self, obj: models.Friendship) -> str:
        """
        FriendshipのFKであるuserのusernameをlist_displayで表示するためのメソッド
        """
        return obj.user.username

    def friend_user_id(self, obj: models.Friendship) -> int:
        """
        FriendshipのFKであるfriendのidをlist_displayで表示するためのメソッド
        """
        return obj.friend.id

    def friend_username(self, obj: models.Friendship) -> str:
        """
        FriendshipのFKであるfriendのusernameをlist_displayで表示するためのメソッド
        """
        return obj.friend.username
