from django.db import models

from tournaments import constants


class Tournament(models.Model):
    """
    トーナメントを管理するモデル

    Attributes:
        status: トーナメントの現在の状態を表す
            - not_stated: 参加者募集中
            - on_going: 進行中
            - completed: 終了
            - canceled: 中止
        created_at: トーナメント作成日時
        updated_at: トーナメント更新日時
    """

    status = models.CharField(
        max_length=15,
        choices=[
            (status.value, status.name)
            for status in constants.TournamentFields.StatusEnum
        ],
        default=constants.TournamentFields.StatusEnum.NOT_STARTED.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tournaments"

    def __str__(self) -> str:
        return f"{self.id}"
