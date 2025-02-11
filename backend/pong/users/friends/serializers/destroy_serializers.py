from rest_framework import serializers

from users import constants as users_constants

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
              - フレンド解除したいユーザーがフレンドではない場合
              - 自分自身をフレンド解除しようとした場合
        """
        user_id: int = data["user"]["id"]
        friend_user_id: int = data["friend"]["id"]

        # 自分自身をフレンド解除しようとした場合にValidationErrorを発生させる
        validators.invalid_same_user_validator(user_id, friend_user_id)

        # フレンド解除したいユーザーとフレンドではない場合にValidationErrorを発生させる
        if not validators.is_friendship_exists(user_id, friend_user_id):
            raise serializers.ValidationError(
                {
                    constants.FriendshipFields.FRIEND_USER_ID: "The user is not a friend."
                },
                code=users_constants.Code.INVALID,
            )
        return data
