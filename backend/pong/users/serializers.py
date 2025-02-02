from rest_framework import serializers

from accounts import constants
from accounts.player import models


class UsersSerializer(serializers.Serializer):
    """
    users app全体で共通のシリアライザ
    Playerとそれに紐づくUserから、返しても良い情報のみをまとめてシリアライズする
    """

    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    display_name = serializers.CharField()
    # todo: こことfieldにavatar追加

    class Meta:
        model = models.Player
        fields = (
            constants.UserFields.ID,
            constants.UserFields.USERNAME,
            constants.PlayerFields.DISPLAY_NAME,
        )
