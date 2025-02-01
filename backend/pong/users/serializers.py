from rest_framework import serializers

import accounts


class UsersSerializer(serializers.Serializer):
    """
    users app全体で共通のシリアライザ
    Playerとそれに紐づくUserから、返しても良い情報のみをまとめてシリアライズする
    """

    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    # todo: fieldにdisplay_name,avatar追加
    # display_name = serializers.CharField()

    class Meta:
        model = accounts.player.models.Player
        fields = (
            accounts.constants.UserFields.ID,
            accounts.constants.UserFields.USERNAME,
        )
