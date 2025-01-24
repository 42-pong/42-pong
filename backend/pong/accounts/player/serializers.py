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
