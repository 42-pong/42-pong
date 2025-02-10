from rest_framework import serializers

from accounts import constants as accounts_constants
from users import serializers as users_serializers

from .. import constants, models


class FriendshipCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", min_value=1)
    friend_user_id = serializers.IntegerField(source="friend.id", min_value=1)
    friend = users_serializers.UsersSerializer(
        source="friend.player",
        read_only=True,
        fields=(  # emailは含めない
            accounts_constants.UserFields.USERNAME,
            accounts_constants.PlayerFields.DISPLAY_NAME,
            # todo: avatar追加
        ),
    )

    class Meta:
        model = models.Friendship
        fields = (
            constants.FriendshipFields.USER_ID,
            constants.FriendshipFields.FRIEND_USER_ID,
            constants.FriendshipFields.FRIEND,
        )

    def create(self, data: dict) -> models.Friendship:
        """
        save()内で呼ばれるcreate()のオーバーライド
        """
        user_id: int = data["user"]["id"]
        friend_user_id: int = data["friend"]["id"]
        return models.Friendship.objects.create(
            user_id=user_id, friend_id=friend_user_id
        )
