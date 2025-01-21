from django.contrib import admin
from django.contrib.admin import ModelAdmin

from . import constants
from .tournament import models as tournament_models


@admin.register(tournament_models.Tournament)
class TournamentAdmin(ModelAdmin):
    """
    adminサイトでtournamentsに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        constants.TournamentFields.ID,
        constants.TournamentFields.STATUS,
        constants.TournamentFields.CREATED_AT,
    )
    search_fields: tuple = (constants.TournamentFields.ID,)
    list_filter: tuple = (constants.TournamentFields.STATUS,)
    ordering: tuple = (
        "-" + constants.TournamentFields.CREATED_AT,
    )  # 降順に表示
