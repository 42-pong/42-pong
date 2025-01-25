import re

from django.contrib.auth.models import User
from rest_framework import serializers

from .. import constants
from . import models


class PlayerSerializer(serializers.ModelSerializer):
    """
    Playerモデルのシリアライザ
    Playerモデルの作成・バリデーションを行う
    """

    # 変数名と同じ名前をfieldsに指定する必要がある

    # PrimaryKeyRelatedField: 紐づくターゲットをそのPKを使用して表現する
    user: serializers.PrimaryKeyRelatedField[User] = (
        serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    )
    # display_nameが渡されなかった場合、"default"という文字列をデフォルト値として設定する
    display_name: serializers.CharField = serializers.CharField(
        max_length=15, default="default"
    )

    class Meta:
        model = models.Player
        fields = (
            constants.PlayerFields.USER,
            constants.PlayerFields.DISPLAY_NAME,
            constants.PlayerFields.CREATED_AT,
            constants.PlayerFields.UPDATED_AT,
        )
        extra_kwargs = {
            constants.PlayerFields.CREATED_AT: {"read_only": True},
            constants.PlayerFields.UPDATED_AT: {"read_only": True},
        }

    def validate_display_name(self, value: str) -> str:
        """
        display_nameフィールドのバリデーション
        英文字・数字・記号(-_.~)のみを許可する
        """
        if not re.match(r"^[a-zA-Z0-9-_.~]+$", value):
            raise serializers.ValidationError(
                "display_name must be alphanumeric or some symbols(-_.~)"
            )
        return value
