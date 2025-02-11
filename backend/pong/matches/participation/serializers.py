from rest_framework import serializers as drf_serializers

from .. import constants
from ..score import serializers as score_serializers
from . import models


class ParticipationSerializer(drf_serializers.ModelSerializer):
    scores = score_serializers.ScoreSerializer(many=True, read_only=True)

    class Meta:
        model = models.Participation
        fields = (
            constants.ParticipationFields.PLAYER_ID,
            constants.ParticipationFields.TEAM,
            constants.ParticipationFields.CREATED_AT,
            "scores",
        )
