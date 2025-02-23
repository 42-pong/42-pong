from rest_framework import serializers as drf_serializers

from .. import constants
from ..round import serializers as round_serializers
from . import models


class TournamentQuerySerializer(drf_serializers.ModelSerializer):
    """
    Tournamentモデルのクエリ(読み取り)操作のためのシリアライザ
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
            constants.TournamentFields.UPDATED_AT,
            "rounds",
        )


class TournamentCommandSerializer(drf_serializers.ModelSerializer):
    """
    Tournamentモデルのコマンド(書き込み)操作のためのシリアライザ
    """

    class Meta:
        model = models.Tournament
        fields = (
            constants.TournamentFields.ID,
            constants.TournamentFields.STATUS,
            constants.TournamentFields.CREATED_AT,
            constants.TournamentFields.UPDATED_AT,
        )
        read_only_fields = (
            constants.TournamentFields.ID,
            constants.TournamentFields.CREATED_AT,
            constants.TournamentFields.UPDATED_AT,
        )
        extra_kwargs = {
            constants.TournamentFields.STATUS: {
                "required": False,
                "default": constants.TournamentFields.StatusEnum.NOT_STARTED.value,
            }
        }

    def validate(self, data: dict) -> dict:
        """
        validate()のオーバーライド関数。

        Raises:
            ValidationError:
                更新時:
                    状態をON_GOINGにするときにまだ参加者がMAX_PARTICIPATIONS人いない場合。
                    状態をCANCELEDにするときにまだ参加者がいる場合。
        """
        # 作成時のバリデーション
        # return data
        new_status = data.get(constants.TournamentFields.STATUS)

        if self.instance:  # 更新時
            # ON_GOING に変更する場合のバリデーション
            if (
                new_status
                == constants.TournamentFields.StatusEnum.ON_GOING.value
            ):
                # MAX_PARTICIPATIONS 人に達していない場合はエラーを発生
                max_participations = (
                    constants.MAX_PARTICIPATIONS
                )  # 定義されている最大参加人数
                current_participants_count = (
                    self.instance.tournament_participations.count()
                )
                if current_participants_count < max_participations:
                    raise drf_serializers.ValidationError(
                        f"Cannot set the status to ON_GOING with less than {max_participations} participants."
                    )
            # CANCELEDに変更する場合のバリデーション
            if (
                self.instance
                and new_status
                == constants.TournamentFields.StatusEnum.CANCELED.value
            ):
                if self.instance.tournament_participations.exists():
                    raise drf_serializers.ValidationError(
                        "Cannot cancel a tournament with participants."
                    )

        return data
