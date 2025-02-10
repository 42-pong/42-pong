from django.contrib import admin
from django.contrib.admin import ModelAdmin

from . import constants
from .match import models as match_models
from .participation import models as participation_models
from .score import models as score_models


@admin.register(match_models.Match)
class MatchAdmin(ModelAdmin):
    """
    adminサイトでmatchに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        constants.MatchFields.ID,
        constants.MatchFields.ROUND_ID,
        constants.MatchFields.CREATED_AT,
    )
    search_fields: tuple = (constants.MatchFields.ROUND_ID,)
    ordering: tuple = ("-" + constants.MatchFields.CREATED_AT,)  # 降順に表示


@admin.register(participation_models.Participation)
class ParticipationAdmin(ModelAdmin):
    """
    adminサイトでmatch_participationsに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        constants.ParticipationFields.ID,
        constants.ParticipationFields.MATCH_ID,
        constants.ParticipationFields.PLAYER_ID,
        constants.ParticipationFields.TEAM,
    )
    search_fields: tuple = (
        constants.ParticipationFields.MATCH_ID,
        constants.ParticipationFields.PLAYER_ID,
    )
    ordering: tuple = (
        "-" + constants.ParticipationFields.CREATED_AT,
    )  # 降順に表示


@admin.register(score_models.Score)
class ScoreAdmin(ModelAdmin):
    """
    adminサイトでscoresに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        constants.ScoreFields.ID,
        constants.ScoreFields.MATCH_PARTICIPATION_ID,
        constants.ScoreFields.CREATED_AT,
        constants.ScoreFields.POS_X,
        constants.ScoreFields.POS_Y,
    )
    search_fields: tuple = (constants.ScoreFields.MATCH_PARTICIPATION_ID,)
    ordering: tuple = ("-" + constants.ScoreFields.CREATED_AT,)  # 降順に表示
