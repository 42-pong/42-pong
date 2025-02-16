from rest_framework import serializers as drf_serializers

from .. import constants
from ..participation import serializers as participation_serializers
from . import models


class MatchSerializer(drf_serializers.ModelSerializer):
    participations = participation_serializers.ParticipationSerializer(
        many=True, read_only=True, source="match_participations"
    )

    class Meta:
        model = models.Match
        fields = (
            constants.MatchFields.ID,
            constants.MatchFields.ROUND_ID,
            constants.MatchFields.STATUS,
            constants.MatchFields.CREATED_AT,
            constants.MatchFields.UPDATED_AT,
            "participations",
        )
