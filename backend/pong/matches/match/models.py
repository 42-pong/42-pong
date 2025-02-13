from django.db import models

from tournaments.round import models as round_models

from .. import constants


class Match(models.Model):
    """
    試合（Match）を表すモデル。
    各試合は特定のラウンド（Round）に属する。

    Attributes:
        round : 関連するラウンドへの外部キー。
        created_at : 試合が作成された日時。
    """

    round = models.ForeignKey(
        round_models.Round,
        on_delete=models.CASCADE,
        related_name="matches",
    )
    status = models.CharField(
        max_length=15,
        choices=[
            (status.value, status.name)
            for status in constants.MatchFields.StatusEnum
        ],
        default=constants.MatchFields.StatusEnum.NOT_STARTED.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "matches"

    def __str__(self) -> str:
        return f"Match {self.id} - Round {self.round.round_number}"
