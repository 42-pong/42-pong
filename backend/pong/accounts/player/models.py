from typing import Any

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ImageField,
    Model,
    OneToOneField,
)
from django.db.models.signals import post_delete
from django.dispatch import receiver

from . import identicon


class Player(Model):
    """
    Playerモデル
    Userモデルと1対1の関係を持つ
    """

    # related_name: 紐づいている他のモデルから逆参照する際の名前(user.playerでPlayerを取得)
    user = OneToOneField(User, on_delete=CASCADE, related_name="player")
    display_name = CharField(max_length=255)
    avatar = ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # ユーザーが認証に使用するfield
    # todo: ログイン/認証機能実装時に確認して変更
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "players"

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """
        Playerインスタンスを保存する際のsave()のオーバーライド
        """
        if not self.avatar:
            # avatar画像のデフォルトを"{username}.png"で生成
            self.avatar = identicon.generate_identicon(self.user.username)
        super().save(*args, **kwargs)


@receiver(post_delete, sender=Player)
def delete_avatar_file(sender: type, instance: Player, **kwargs: Any) -> None:
    """
    シグナルを使用してPlayer削除時にavatar画像も削除する
    """
    if instance.avatar:
        instance.avatar.delete(save=False)
