from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .blocks import constants as blocks_constants
from .blocks import models as blocks_models
from .friends import constants as friends_constants
from .friends import models as friends_models


@admin.register(friends_models.Friendship)
class FriendshipAdmin(ModelAdmin):
    """
    Friendshipのadminサイト用設定
    """

    list_display: tuple = (
        friends_constants.FriendshipFields.ID,
        friends_constants.FriendshipFields.USER_ID,
        "username",
        friends_constants.FriendshipFields.FRIEND_USER_ID,
        "friend_username",
        friends_constants.FriendshipFields.CREATED_AT,
        friends_constants.FriendshipFields.UPDATED_AT,
    )
    search_fields: tuple = (
        "user__id",
        "user__username",
        "friend__id",
        "friend__username",
    )
    list_filter: tuple = (
        "user__id",
        friends_constants.FriendshipFields.CREATED_AT,
        friends_constants.FriendshipFields.UPDATED_AT,
    )
    ordering: tuple = (f"-{friends_constants.FriendshipFields.CREATED_AT}",)

    def username(self, obj: friends_models.Friendship) -> str:
        """
        FriendshipのFKであるuserのusernameをlist_displayで表示するためのメソッド
        """
        return obj.user.username

    def friend_user_id(self, obj: friends_models.Friendship) -> int:
        """
        FriendshipのFKであるfriendのidをlist_displayで表示するためのメソッド
        """
        return obj.friend.id

    def friend_username(self, obj: friends_models.Friendship) -> str:
        """
        FriendshipのFKであるfriendのusernameをlist_displayで表示するためのメソッド
        """
        return obj.friend.username


@admin.register(blocks_models.BlockRelationship)
class BlockRelationshipAdmin(ModelAdmin):
    """
    BlockRelationshipのadminサイト用設定
    """

    list_display: tuple = (
        blocks_constants.BlockRelationshipFields.ID,
        blocks_constants.BlockRelationshipFields.USER_ID,
        "username",
        blocks_constants.BlockRelationshipFields.BLOCKED_USER_ID,
        "blocked_username",
        blocks_constants.BlockRelationshipFields.CREATED_AT,
        blocks_constants.BlockRelationshipFields.UPDATED_AT,
    )
    search_fields: tuple = (
        "user__id",
        "user__username",
        "blocked_user__id",
        "blocked_user__username",
    )
    list_filter: tuple = (
        "user__id",
        blocks_constants.BlockRelationshipFields.CREATED_AT,
        blocks_constants.BlockRelationshipFields.UPDATED_AT,
    )
    ordering: tuple = (
        f"-{blocks_constants.BlockRelationshipFields.CREATED_AT}",
    )

    def username(self, obj: blocks_models.BlockRelationship) -> str:
        """
        BlockRelationshipのFKであるuserのusernameをlist_displayで表示するためのメソッド
        """
        return obj.user.username

    def blocked_username(self, obj: blocks_models.BlockRelationship) -> str:
        """
        BlockRelationshipのFKであるblocked_userのusernameをlist_displayで表示するためのメソッド
        """
        return obj.blocked_user.username
