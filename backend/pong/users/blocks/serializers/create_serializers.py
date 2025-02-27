from rest_framework import serializers

from accounts import constants as accounts_constants
from users import constants as users_constants
from users import serializers as users_serializers

from .. import constants, models
from . import validators


class BlockRelationshipCreateSerializer(serializers.ModelSerializer):
    blocked_user_id = serializers.IntegerField(
        source="blocked_user.id", min_value=1, write_only=True
    )
    blocked_user = users_serializers.UsersSerializer(
        source="blocked_user.player",
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
        model = models.BlockRelationship
        fields = (
            constants.BlockRelationshipFields.BLOCKED_USER_ID,
            constants.BlockRelationshipFields.BLOCKED_USER,
        )

    def create(self, data: dict) -> models.BlockRelationship:
        """
        save()内で呼ばれるcreate()のオーバーライド
        """
        user_id: int = self.context[constants.BlockRelationshipFields.USER_ID]
        blocked_user_id: int = data[
            constants.BlockRelationshipFields.BLOCKED_USER
        ][constants.BlockRelationshipFields.ID]
        return models.BlockRelationship.objects.create(
            user_id=user_id, blocked_user_id=blocked_user_id
        )

    def validate(self, data: dict) -> dict:
        """
        is_valid()内で呼ばれるvalidate()のオーバーライド

        Raises:
            serializers.ValidationError
              - 自分自身をブロックしようとした場合
              - ブロックしたいユーザーが存在しない場合
              - ブロックしたいユーザーを既にブロックしている場合
        """
        user_id: int = self.context[constants.BlockRelationshipFields.USER_ID]
        blocked_user_id: int = data[
            constants.BlockRelationshipFields.BLOCKED_USER
        ][constants.BlockRelationshipFields.ID]

        # 自分自身をブロックしようとした場合にValidationErrorを発生させる
        validators.invalid_same_user_validator(user_id, blocked_user_id)

        # ブロックしたいユーザーを既にブロックしている場合にValidationErrorを発生させる
        validators.already_block_validator(user_id, blocked_user_id)

        return data
