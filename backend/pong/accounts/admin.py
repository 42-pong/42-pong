from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from . import constants
from .player import models as player_models
from .two_factor_authentication.otp import constants as otp_constants
from .two_factor_authentication.otp import models as otp_models
from .two_factor_authentication.temporary_user import (
    models as temporary_user_models,
)


# todo: Userモデルに関するカスタマイズは専用のファイルに移動した方が良いのかも
class CustomUserAdmin(UserAdmin):
    """
    adminサイトのUsersに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        constants.UserFields.ID,
        constants.UserFields.USERNAME,
        constants.UserFields.EMAIL,
        "is_superuser",
        "is_staff",
        "is_active",
    )


# デフォルトのUserModelの登録を解除して、カスタマイズしたUserAdminクラスで再登録
# adminサイトにカスタマイズされたlist_displayが表示されるようになる
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(player_models.Player)
class AccountAdmin(ModelAdmin):
    """
    adminサイトでPlayersに表示されるカラムをカスタマイズ
    """

    # Playerに紐づくUserの情報をadminサイトで表示する為にはメソッド名をそのまま指定
    # メソッド名はアンダースコアがスペースに変換されてカラム名として扱われる
    list_display: tuple = (
        constants.PlayerFields.ID,
        "user_id",
        "username",
        constants.PlayerFields.DISPLAY_NAME,
        constants.PlayerFields.AVATAR,
        constants.PlayerFields.CREATED_AT,
        constants.PlayerFields.UPDATED_AT,
    )
    list_filter: tuple = (constants.PlayerFields.UPDATED_AT,)
    search_fields: tuple = (
        f"{constants.PlayerFields.USER}__{constants.UserFields.USERNAME}",
        constants.PlayerFields.DISPLAY_NAME,
    )

    def user_id(self, obj: player_models.Player) -> int:
        """
        Playerと1対1関係にあるUserのIDをlist_displayで表示するためのメソッド
        """
        return obj.user.id

    def username(self, obj: player_models.Player) -> str:
        """
        Playerと1対1関係にあるUserのusernameをlist_displayで表示するためのメソッド
        """
        return obj.user.username


@admin.register(otp_models.OTP)
class OTPAdmin(ModelAdmin):
    """
    adminサイトでOtpsに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        otp_constants.OptFields.ID,
        otp_constants.OptFields.TEMP_USER_ID,
        otp_constants.OptFields.OTP_CODE,
        otp_constants.OptFields.CREATED_AT,
    )
    list_filter: tuple = (otp_constants.OptFields.CREATED_AT,)
    search_fields: tuple = (otp_constants.OptFields.TEMP_USER_ID,)


@admin.register(temporary_user_models.TemporaryUser)
class TemporaryUserAdmin(ModelAdmin):
    """
    adminサイトでTemporary usersに表示されるカラムをカスタマイズ
    """

    list_display: tuple = (
        constants.UserFields.ID,
        constants.UserFields.EMAIL,
        constants.UserFields.PASSWORD,
    )
    list_filter: tuple = (constants.UserFields.EMAIL,)
    search_fields: tuple = (constants.UserFields.EMAIL,)
