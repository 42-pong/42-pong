from django.contrib import admin

from .constants import PlayerFields, UserFields
from .models import Player


@admin.register(Player)
class AccountAdmin(admin.ModelAdmin):
    """
    adminサイトでPlayersに表示されるカラムをカスタマイズ
    """

    # Playerに紐づくUserの情報をadminサイトで表示する為にはメソッド名をそのまま指定
    # メソッド名はアンダースコアがスペースに変換されてカラム名として扱われる
    # todo: Player特有のfieldが追加されたらそれらも追加する
    list_display: tuple = (
        "user_id",
        "username",
        PlayerFields.CREATED_AT,
        PlayerFields.UPDATED_AT,
    )
    list_filter: tuple = (PlayerFields.UPDATED_AT,)
    search_fields: tuple = (f"{PlayerFields.USER}__{UserFields.USERNAME}",)

    def user_id(self, obj: Player) -> int:
        """
        Playerと1対1関係にあるUserのIDをlist_displayで表示するためのメソッド
        """
        return obj.user.id

    def username(self, obj: Player) -> str:
        """
        Playerと1対1関係にあるUserのusernameをlist_displayで表示するためのメソッド
        """
        return obj.user.username
