from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from . import models


class ReadOnlyAdmin(admin.ModelAdmin):
    """
    管理サイトでのインスタンスの作成・変更を禁止する基底クラス。
    """

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        管理サイトでのインスタンスの追加を禁止にする関数。
        """
        return False

    # objの型定義がドキュメントみても書いていなかったので型をAnyにしました
    def has_change_permission(
        self, request: HttpRequest, obj: Any = None
    ) -> bool:
        """
        管理サイトでのインスタンスの変更を禁止にする関数。
        """
        return False


@admin.register(models.OAuth2)
class OAuth2Admin(ReadOnlyAdmin):
    list_display = (
        "provider",
        "provider_id",
        "created_at",
    )


@admin.register(models.FortyTwoToken)
class FortyTwoTokenAdmin(ReadOnlyAdmin):
    # トークン情報の漏れを防ぐため、アクセストークンとリフレッシュトークンを公開しない
    exclude = ("access_token", "refresh_token")
    list_display = (
        "oauth2",
        "access_token_expiry",
        "created_at",
    )
    list_filter = ("created_at",)
