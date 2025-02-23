from rest_framework import serializers

from .. import constants
from . import models


class ParticipationQuerySerializer(serializers.ModelSerializer):
    """
    Participationモデルのクエリ(読み取り)操作のためのシリアライザ
    """

    user_id = serializers.IntegerField(source="player.user.id", read_only=True)

    class Meta:
        model = models.Participation
        fields = (
            constants.ParticipationFields.ID,
            constants.ParticipationFields.TOURNAMENT_ID,
            "user_id",
            constants.ParticipationFields.PARTICIPATION_NAME,
            constants.ParticipationFields.RANKING,
            constants.ParticipationFields.CREATED_AT,
            constants.ParticipationFields.UPDATED_AT,
        )

    # TODO: rankingに渡される値が正確かどうかのバリデーション実装
    # TODO: rankingをrequired=False, default=Noneを追加
    # TODO: participation_nameが空だったらエラー
    # TODO: UniqueTogetherValidatorを追加
