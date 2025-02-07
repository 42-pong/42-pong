from rest_framework import serializers as drf_serializers

from .. import constants, models


class FriendshipListSerializer(drf_serializers.ModelSerializer):
    user_id = drf_serializers.IntegerField(
        source="user.id", min_value=1, read_only=True
    )
    friend_user_id = drf_serializers.IntegerField(
        source="friend.id", min_value=1, read_only=True
    )

    class Meta:
        model = models.Friendship
        fields = (
            constants.FriendshipFields.USER_ID,
            constants.FriendshipFields.FRIEND_USER_ID,
        )
