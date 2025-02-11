from rest_framework import serializers

from .. import constants, models
from . import validators


class FriendshipDestroySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", min_value=1)
    friend_user_id = serializers.IntegerField(source="friend.id", min_value=1)

    class Meta:
        model = models.Friendship
        fields = (
            constants.FriendshipFields.USER_ID,
            constants.FriendshipFields.FRIEND_USER_ID,
        )

    def validate(self, data: dict) -> dict:
        """
        is_valid()内で呼ばれるvalidate()のオーバーライド

        Raises:
            serializers.ValidationError
              - 自分自身をフレンド解除しようとした場合
        """
        user_id: int = data["user"]["id"]
        friend_user_id: int = data["friend"]["id"]

        # 自分自身をフレンド解除しようとした場合にValidationErrorを発生させる
        validators.invalid_same_user_validator(user_id, friend_user_id)
        return data
