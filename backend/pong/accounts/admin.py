from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import models as auth_models

from .constants import PlayerFields, UserFields
from .models import Player


# todo: Userモデルに関するカスタマイズは専用のファイルに移動した方が良いのかも
class CustomUserAdmin(auth_admin.UserAdmin):
    """
    adminサイトのUsersに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        UserFields.ID,
        UserFields.USERNAME,
        UserFields.EMAIL,
        "is_superuser",
        "is_staff",
        "is_active",
    )


# デフォルトのUserModelの登録を解除して、カスタマイズしたUserAdminクラスで再登録
# adminサイトにカスタマイズされたlist_displayが表示されるようになる
admin.site.unregister(auth_models.User)
admin.site.register(auth_models.User, CustomUserAdmin)


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
