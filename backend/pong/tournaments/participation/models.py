from django.db import models

import accounts
from tournaments.tournament import models as tournament_models


class Participation(models.Model):
    """
    PlayerのTournament参加情報モデル
    TournamentとPlayerに対して多対一の関係を持つ

    Attributes:
        id: 識別子
        tournament_id: トーナメントテーブルの外部キー
        player_id: プレーヤーテーブルの外部キー
        participation_name: 参加したトーナメントにおける表示名
        created_at: トーナメント参加日時
        updated_at: トーナメント順位更新日時
        ranking: 参加したトーナメントにおける最終順位
    """

    id = models.BigAutoField(primary_key=True)
    tournament_id = models.ForeignKey(
        tournament_models.Tournament,
        related_name="participants",  # Tournamentsからこのテーブルにアクセスするときにエイリアス名
        on_delete=models.CASCADE,
        db_column="tournament_id",
    )
    player_id = models.ForeignKey(
        accounts.player.models.Player,
        related_name="tournament_participations",  # Playersからこのテーブルにアクセスするときにエイリアス名
        on_delete=models.CASCADE,
        db_column="player_id",
    )
    participation_name = models.CharField(max_length=255)
    ranking = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tournament_participations"
        constraints = [
            models.UniqueConstraint(
                fields=["tournament_id", "player_id"],
                name="unique_tournament_participation",
            )
        ]

    def __str__(self) -> str:
        return self.participation_name
