from rest_framework import serializers

from accounts.player.models import Player
from tournaments.tournament.models import Tournament

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


class ParticipationCommandSerializer(serializers.ModelSerializer):
    """
    Participationモデルのコマンド(書き込み)操作のためのシリアライザ
    """

    tournament_id = serializers.PrimaryKeyRelatedField(
        queryset=Tournament.objects.all(), source="tournament"
    )
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source="player"
    )

    class Meta:
        model = models.Participation
        fields = (
            constants.ParticipationFields.ID,
            constants.ParticipationFields.TOURNAMENT_ID,
            constants.ParticipationFields.PLAYER_ID,
            constants.ParticipationFields.PARTICIPATION_NAME,
            constants.ParticipationFields.RANKING,
        )
        extra_kwargs = {
            constants.ParticipationFields.TOURNAMENT_ID: {
                "required": True,
            },
            constants.ParticipationFields.PLAYER_ID: {
                "required": True,
            },
            constants.ParticipationFields.PARTICIPATION_NAME: {
                "required": True,
            },
            constants.ParticipationFields.RANKING: {
                "required": False,
                "allow_null": True,
                "default": None,
            },
        }
        # ユニーク制約を追加
        # TODO: なぜか効かなくて図っと詰まってしまったのでいったんモデルの方で行う
        # validators = [
        #    UniqueTogetherValidator(
        #        queryset=models.Participation.objects.all(),
        #        fields=(
        #            constants.ParticipationFields.TOURNAMENT_ID,
        #            constants.ParticipationFields.PLAYER_ID,
        #        ),
        #        message="このトーナメントとプレイヤーの組み合わせは既に存在します。",
        #    )
        # ]
