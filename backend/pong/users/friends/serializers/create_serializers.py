from rest_framework import serializers

from accounts import constants as accounts_constants
from users import constants as users_constants
from users import serializers as users_serializers

from .. import constants, models
from . import validators


class FriendshipCreateSerializer(serializers.ModelSerializer):
    friend_user_id = serializers.IntegerField(
        source="friend.id", min_value=1, write_only=True
    )
    friend = users_serializers.UsersSerializer(
        source="friend.player",
        read_only=True,
        fields=(  # emailは含めない
            accounts_constants.UserFields.ID,
            accounts_constants.UserFields.USERNAME,
            accounts_constants.PlayerFields.DISPLAY_NAME,
            accounts_constants.PlayerFields.AVATAR,
            users_constants.UsersFields.IS_FRIEND,
            users_constants.UsersFields.IS_BLOCKED,
            users_constants.UsersFields.MATCH_WINS,
            users_constants.UsersFields.MATCH_LOSSES,
        ),
    )

    class Meta:
        model = models.Friendship
        fields = (
            constants.FriendshipFields.FRIEND_USER_ID,
            constants.FriendshipFields.FRIEND,
        )

    def create(self, data: dict) -> models.Friendship:
        """
        save()内で呼ばれるcreate()のオーバーライド
        """
        user_id: int = self.context[constants.FriendshipFields.USER_ID]
        friend_user_id: int = data["friend"]["id"]
        return models.Friendship.objects.create(
            user_id=user_id, friend_id=friend_user_id
        )

    def validate(self, data: dict) -> dict:
        """
        is_valid()内で呼ばれるvalidate()のオーバーライド

        Raises:
            serializers.ValidationError
              - 自分自身をフレンドに追加しようとした場合
              - フレンドに追加したいユーザーが存在しない場合
              - フレンドに追加したいユーザーが既にフレンドである場合
        """
        user_id: int = self.context[constants.FriendshipFields.USER_ID]
        friend_user_id: int = data["friend"]["id"]

        # 自分自身をフレンドに追加しようとした場合にValidationErrorを発生させる
        validators.invalid_same_user_validator(user_id, friend_user_id)

        # フレンドに追加したいユーザーが既にフレンドである場合にValidationErrorを発生させる
        validators.already_friend_validator(user_id, friend_user_id)

        return data
