from django.core.validators import RegexValidator
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
    participation_name: serializers.CharField = serializers.CharField(
        max_length=15,
        validators=[
            # 使用可能文字列を指定: 英子文字・英大文字・数字・記号(-_.~)
            RegexValidator(
                regex=r"^[a-zA-Z0-9-_.~]+$",
                message="Must contain only alphanumeric characters or some symbols(-_.~)",
            )
        ],
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

    def validate(self, data: dict) -> dict:
        """
        validate()のオーバーライド関数。

        Raises:
            ValidationError:
                作成時:
                    すでに参加者がMAX＿PARTICIPATION分いる場合。
        """
        if self.instance is None:  # 新規作成時
            tournament_id = data.get("tournament")
            if tournament_id is not None:
                # 紐づくトーナメントに関連する参加者数をカウント
                participation_count = models.Participation.objects.filter(
                    tournament_id=tournament_id
                ).count()
                if participation_count >= constants.MAX_PARTICIPATIONS:
                    raise serializers.ValidationError(
                        f"This tournament already has the maximum number of participants ({constants.MAX_PARTICIPATIONS})."
                    )

        return data

    def validate_ranking(self, value: int) -> int:
        if value is not None and (
            value < 1 or value > constants.MAX_PARTICIPATIONS
        ):
            raise serializers.ValidationError(
                f"Ranking must be between 1 and {constants.MAX_PARTICIPATIONS}."
            )
        return value
