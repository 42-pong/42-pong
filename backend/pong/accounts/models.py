from django.contrib.auth.models import User
from django.db.models import CASCADE, DateTimeField, Model, OneToOneField


# todo: 表示名・アバター画像PATHなどがfieldに追加される予定
class Player(Model):
    """
    Playerモデル
    Userモデルと1対1の関係を持つ
    """

    user = OneToOneField(User, on_delete=CASCADE, related_name="player")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # ユーザーが認証に使用するfield
    # todo: ログイン/認証機能実装時に確認して変更
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "players"

    def __str__(self) -> str:
        return self.user.username
