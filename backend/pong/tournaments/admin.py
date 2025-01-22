from django.contrib import admin
from django.contrib.admin import ModelAdmin

from . import constants
from .participation import models as participation_models
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


@admin.register(participation_models.Participation)
class ParticipationAdmin(ModelAdmin):
    """
    adminサイトでtournament_participationsに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        constants.ParticipationFields.ID,
        constants.ParticipationFields.TOURNAMENT_ID,
        constants.ParticipationFields.PLAYER_ID,
        constants.ParticipationFields.PARTICIPATION_NAME,
        constants.ParticipationFields.JOINED_AT,
        constants.ParticipationFields.RANKING,
    )
    search_fields: tuple = (constants.ParticipationFields.PARTICIPATION_NAME,)
    list_filter: tuple = (constants.ParticipationFields.RANKING,)
    ordering: tuple = (
        "-" + constants.ParticipationFields.JOINED_AT,
    )  # 降順に表示
