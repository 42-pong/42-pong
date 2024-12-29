from django.contrib import admin

from . import models


@admin.register(models.OAuth2)
class OAuth2Admin(admin.ModelAdmin):
    list_display = (
        "provider",
        "provider_id",
        "created_at",
    )


@admin.register(models.FortyTwoToken)
class FortyTwoTokenAdmin(admin.ModelAdmin):
    # トークン情報の漏れを防ぐため、アクセストークンとリフレッシュトークンを公開しない
    exclude = ("access_token", "refresh_token")
    list_display = (
        "user",
        "access_token_expiry",
        "created_at",
    )
    list_filter = ("created_at",)

