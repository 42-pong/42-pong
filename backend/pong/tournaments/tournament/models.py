from django.db import models

from tournaments import constants


class Tournament(models.Model):
    """
    Tournamentのモデル
    """

    status = models.CharField(
        max_length=10,
        choices=[
            (status.value, status.name)
            for status in constants.TournamentFields.StatusEnum
        ],
        default=constants.TournamentFields.StatusEnum.MATCHING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tournaments"
