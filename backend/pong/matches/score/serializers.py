from rest_framework import serializers as drf_serializers

from .. import constants
from . import models


class ScoreSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = models.Score
        fields = (
            constants.ScoreFields.CREATED_AT,
            constants.ScoreFields.POS_X,
            constants.ScoreFields.POS_Y,
        )
