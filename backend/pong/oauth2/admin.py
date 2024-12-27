from django.contrib import admin

from .models import FortyTwoToken


@admin.register(FortyTwoToken)
class FortyTwoTokenAdmin(admin.ModelAdmin):
    # トークン情報の漏れを防ぐため、アクセストークンとリフレッシュトークンを公開しない
    exclude = ("access_token", "refresh_token")
    list_display = (
        "user",
        "access_token_expiry",
        "created_at",
    )
    list_filter = ("created_at",)

    def has_add_permission(self, request) -> bool:
        """
        管理サイトでのFortyTwoTokenAdminのインスタンスを追加する権限を拒否します。
        """
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """
        管理サイトでのFortyTwoTokenAdminのインスタンスを変更する権限を拒否します。
        """
        return False
