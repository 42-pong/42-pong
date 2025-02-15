from rest_framework import serializers as drf_serializers

from accounts import constants as accounts_constants
from users import serializers as users_serializers

from .. import constants, models


class FriendshipListSerializer(drf_serializers.ModelSerializer):
    friend = users_serializers.UsersSerializer(
        source="friend.player",
        read_only=True,
        fields=(  # emailは含めない
            accounts_constants.UserFields.USERNAME,
            accounts_constants.PlayerFields.DISPLAY_NAME,
            accounts_constants.PlayerFields.AVATAR,
        ),
    )

    class Meta:
        model = models.Friendship
        fields = (constants.FriendshipFields.FRIEND,)
