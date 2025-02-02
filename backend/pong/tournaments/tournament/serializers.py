from rest_framework import serializers

from . import models


class TournamentSerializer(serializers.ModelSerializer):
    """
    Tournamentモデルのシリアライザ
    """

    # TODO: 後で実装
    class Meta:
        model = models.Tournament
        fields = "__all__"
