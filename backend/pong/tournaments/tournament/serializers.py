from rest_framework import serializers as drf_serializers

from .. import constants
from ..round import serializers as round_serializers
from . import models


class TournamentSerializer(drf_serializers.ModelSerializer):
    """
    Tournamentモデルのシリアライザ
    """

    rounds = round_serializers.RoundSerializer(
        many=True, read_only=True, source="round"
    )

    class Meta:
        model = models.Tournament
        fields = (
            constants.TournamentFields.ID,
            constants.TournamentFields.STATUS,
            constants.TournamentFields.CREATED_AT,
            "rounds",
        )
