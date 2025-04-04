from rest_framework import serializers

from .. import constants, models
from . import validators


class FriendshipDestroySerializer(serializers.ModelSerializer):
    friend_user_id = serializers.IntegerField(
        source="friend.id", min_value=1, write_only=True
    )

    class Meta:
        model = models.Friendship
        fields = (constants.FriendshipFields.FRIEND_USER_ID,)

    def validate(self, data: dict) -> dict:
        """
        is_valid()内で呼ばれるvalidate()のオーバーライド

        Raises:
            serializers.ValidationError
              - フレンド解除したいユーザーがフレンドではない場合
              - 自分自身をフレンド解除しようとした場合
              - フレンド解除したいユーザーが存在しない場合
        """
        user_id: int = self.context[constants.FriendshipFields.USER_ID]
        friend_user_id: int = data["friend"]["id"]

        # 自分自身をフレンド解除しようとした場合にValidationErrorを発生させる
        validators.invalid_same_user_validator(user_id, friend_user_id)

        # フレンド解除したいユーザーとフレンドではない場合にValidationErrorを発生させる
        validators.not_friend_validator(user_id, friend_user_id)

        return data
