from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from . import models
from .constants import PlayerFields, UserFields


# todo: Userモデルに関するカスタマイズは専用のファイルに移動した方が良いのかも
class CustomUserAdmin(UserAdmin):
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
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(models.Player)
class AccountAdmin(ModelAdmin):
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

    def user_id(self, obj: models.Player) -> int:
        """
        Playerと1対1関係にあるUserのIDをlist_displayで表示するためのメソッド
        """
        return obj.user.id

    def username(self, obj: models.Player) -> str:
        """
        Playerと1対1関係にあるUserのusernameをlist_displayで表示するためのメソッド
        """
        return obj.user.username
