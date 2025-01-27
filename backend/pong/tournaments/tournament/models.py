from django.db import models

from tournaments import constants


class Tournament(models.Model):
    """
    トーナメントを管理するモデル

    Attributes:
        status: トーナメントの現在の状態を表す
            - matching: 参加者募集中
            - playing: 進行中
            - end: 終了済み
        created_at: トーナメント作成日時
    """

    status = models.CharField(
        max_length=10,
        choices=[
            (status.value, status.name)
            for status in constants.TournamentFields.StatusEnum
        ],
        default=constants.TournamentFields.StatusEnum.MATCHING.value,
        # TODO: db_index=Trueを必要によって追加
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tournaments"

    def __str__(self) -> str:
        return f"{self.id}"
