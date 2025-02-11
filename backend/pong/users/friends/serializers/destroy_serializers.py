from rest_framework import serializers

from .. import constants, models


class FriendshipDestroySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", min_value=1)
    friend_user_id = serializers.IntegerField(source="friend.id", min_value=1)

    class Meta:
        model = models.Friendship
        fields = (
            constants.FriendshipFields.USER_ID,
            constants.FriendshipFields.FRIEND_USER_ID,
        )
