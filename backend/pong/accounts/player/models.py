from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    Model,
    OneToOneField,
)


# todo: アバター画像PATHがfieldに追加される予定
class Player(Model):
    """
    Playerモデル
    Userモデルと1対1の関係を持つ
    """

    # related_name: 紐づいている他のモデルから逆参照する際の名前(user.playerでPlayerを取得)
    user = OneToOneField(User, on_delete=CASCADE, related_name="player")
    display_name = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # ユーザーが認証に使用するfield
    # todo: ログイン/認証機能実装時に確認して変更
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "players"

    def __str__(self) -> str:
        return self.user.username
