from django.contrib import admin

from . import models
from .constants import PlayerFields, UserFields


@admin.register(models.Player)
class AccountAdmin(admin.ModelAdmin):
    """
    Playerモデルの管理画面をカスタマイズする
    """

    list_display = (
        PlayerFields.ID,
        PlayerFields.USER,
        PlayerFields.CREATED_AT,
        PlayerFields.UPDATED_AT,
    )
    list_filter = (PlayerFields.UPDATED_AT,)
    search_fields = (
        f"{PlayerFields.USER}__{UserFields.USERNAME}",
        f"{PlayerFields.USER}__{UserFields.EMAIL}",
    )
