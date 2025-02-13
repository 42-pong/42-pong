from rest_framework import serializers as drf_serializers

from matches.match import serializers as match_serializers

from .. import constants
from . import models


class RoundSerializer(drf_serializers.ModelSerializer):
    """
    Roundモデルのシリアライザ
    """

    matches = match_serializers.MatchSerializer(many=True, read_only=True)

    class Meta:
        model = models.Round
        fields = (
            constants.RoundFields.ROUND_NUMBER,
            constants.RoundFields.STATUS,
            constants.RoundFields.CREATED_AT,
            constants.RoundFields.UPDATED_AT,
            "matches",
        )
