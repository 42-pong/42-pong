from django.db import models

from matches.participation import models as participation_models


class Score(models.Model):
    """
    試合におけるスコア（Score）を表すモデル。
    各スコアは特定のプレイヤーの試合参加情報に紐づく。

    Attributes:
        participation : スコアを記録したプレイヤーの参加情報。
        created_at : スコアが記録された日時。
        pos_x : スコアが発生したX座標。
        pos_y : スコアが発生したY座標。
    """

    match_participation = models.ForeignKey(
        participation_models.Participation,
        on_delete=models.CASCADE,
        related_name="scores",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()

    class Meta:
        db_table = "scores"

    def __str__(self) -> str:
        return f"Score {self.id} for player={self.match_participation.player.display_name} at {self.created_at}"
