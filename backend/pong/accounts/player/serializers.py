from django.contrib.auth.models import User
from rest_framework import serializers

from .. import constants
from . import models


class PlayerSerializer(serializers.ModelSerializer):
    """
    Playerモデルのシリアライザ
    Playerモデルの作成・バリデーションを行う
    """

    # PrimaryKeyRelatedField: 紐づくターゲットをそのPKを使用して表現する
    # 同じ変数名(user)をfieldsに指定する必要がある
    user: serializers.PrimaryKeyRelatedField[User] = (
        serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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

    # todo: Playerモデルにfieldが追加されたらvalidate(),create()を作成する
