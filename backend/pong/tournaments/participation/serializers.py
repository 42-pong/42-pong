from rest_framework import serializers

from . import models


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = "__all__"

    # TODO: rankingに渡される値が正確かどうかのバリデーション実装
    # TODO: rankingをrequired=False, default=Noneを追加
    # TODO: participation_nameが空だったらエラー
