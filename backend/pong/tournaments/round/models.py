from django.db import models

from tournaments.tournament import models as tournament_models

from .. import constants


class Round(models.Model):
    """
    Tournament（トーナメント）の各ラウンドを表すモデル。

    各ラウンドは特定のトーナメント（tournament_id）に紐づき、
    ラウンド番号（round_number）とステータス（status）を持つ。

    Attributes:
        tournament : 関連するトーナメントへの外部キー
        round_number  : トーナメント内でのラウンドの番号（1以上）
        status: ラウンドの現在の状態を表す
            - not_stated: 開始前
            - on_going: 進行中
            - completed: 終了
            - canceled: 中止
        created_at    : レコードの作成日時
        updated_at    : レコードの最終更新日時
    """

    id = models.BigAutoField(primary_key=True)
    tournament = models.ForeignKey(
        tournament_models.Tournament,
        related_name="round",  # Tournamentsからこのテーブルにアクセスするときにエイリアス名
        on_delete=models.CASCADE,
    )
    round_number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=15,
        choices=[
            (status.value, status.name)
            for status in constants.RoundFields.StatusEnum
        ],
        default=constants.RoundFields.StatusEnum.NOT_STARTED.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rounds"

    def __str__(self) -> str:
        return f"Round {self.round_number} (Tournament ID: {self.tournament_id}) - {self.status}"
