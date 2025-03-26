from rest_framework import serializers as drf_serializers

from .. import constants
from ..score import serializers as score_serializers
from . import models


class ParticipationSerializer(drf_serializers.ModelSerializer):
    user_id = drf_serializers.IntegerField(
        source="player.user.id", read_only=True
    )
    scores = score_serializers.ScoreSerializer(many=True, read_only=True)

    class Meta:
        model = models.Participation
        fields = (
            # 作成時間や更新時間はあまり重要ではないので送らない
            "user_id",
            constants.ParticipationFields.TEAM,
            constants.ParticipationFields.IS_WIN,
            "scores",
        )
