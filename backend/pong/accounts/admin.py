from django.contrib import admin

from .models import Player


@admin.register(Player)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "user__username",
        "user__email",
    )
