from django.contrib import admin

from .constants import PlayerFields, UserFields
from .models import Player


@admin.register(Player)
class AccountAdmin(admin.ModelAdmin):
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
