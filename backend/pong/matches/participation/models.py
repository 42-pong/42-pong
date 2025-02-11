from django.db import models

import accounts.player.models as player_models
from matches.match import models as match_models

from .. import constants


class Participation(models.Model):
    """
    試合の参加者（MatchParticipation）を表すモデル。
    各試合におけるプレイヤーの情報を管理する。

    Attributes:
        match : 参加している試合への外部キー。
        player : 参加するプレイヤーへの外部キー。
        team : プレイヤーが所属するチーム（"1", "2"）。
        created_at : 参加情報が作成された日時。
    """

    match = models.ForeignKey(
        match_models.Match,
        on_delete=models.CASCADE,
        related_name="match_participations",
    )
    player = models.ForeignKey(
        player_models.Player,
        on_delete=models.CASCADE,
        related_name="match_participations",
    )
    team = models.CharField(
        max_length=15,
        choices=[
            (status.value, status.name)
            for status in constants.ParticipationFields.TeamEnum
        ],
        default=constants.ParticipationFields.TeamEnum.ONE.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "match_participations"
        constraints = [
            models.UniqueConstraint(
                fields=["match_id", "player_id"],
                name="unique_match_participation",
            )
        ]

    def __str__(self) -> str:
        return f"Player={self.player.display_name} in match_id={self.match.id}, team=({self.team})"
