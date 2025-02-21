from rest_framework import serializers

from .. import constants, models
from . import validators


class BlockRelationshipDestroySerializer(serializers.ModelSerializer):
    blocked_user_id = serializers.IntegerField(
        source="blocked_user.id", min_value=1, write_only=True
    )

    class Meta:
        model = models.BlockRelationship
        fields = (constants.BlockRelationshipFields.BLOCKED_USER_ID,)

    def validate(self, data: dict) -> dict:
        """
        is_valid()内で呼ばれるvalidate()のオーバーライド

        Raises:
            serializers.ValidationError
              - ブロック解除したいユーザーをブロックしていない場合
              - 自分自身をブロック解除しようとした場合
              - ブロック解除したいユーザーが存在しない場合
        """
        user_id: int = self.context[constants.BlockRelationshipFields.USER_ID]
        blocked_user_id: int = data[
            constants.BlockRelationshipFields.BLOCKED_USER
        ][constants.BlockRelationshipFields.ID]

        # 自分自身をブロック解除しようとした場合にValidationErrorを発生させる
        validators.invalid_same_user_validator(user_id, blocked_user_id)

        # ブロック解除したいユーザーをブロックしていない場合にValidationErrorを発生させる
        validators.not_block_validator(user_id, blocked_user_id)

        return data
