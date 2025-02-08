from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from . import constants


class Friendship(models.Model):
    """
    フレンド関係を表すモデル
    user: フレンドに追加する側のユーザー
    friend: フレンドに追加される側のユーザー
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships",
        db_column=constants.FriendshipFields.USER_ID,
    )
    friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships_of",
        db_column=constants.FriendshipFields.FRIEND_USER_ID,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "friendships"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "friend"], name="unique_friendship"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} added {self.friend.username} as a friend"

    def clean(self) -> None:
        """
        save()される前にバリデーションを行うclean()のオーバーライド
        """
        # 自分自身をフレンドに追加しようとした場合はエラー
        if self.user == self.friend:
            raise ValidationError("You cannot add yourself as a friend.")
        super().clean()

    # args,kwargsは型ヒントが複雑かつそのままsuper()に渡したいためignoreで対処
    def save(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """
        save()のオーバーライド
        保存する前にcleanメソッドを明示的に呼び出す必要がある
        """
        self.full_clean()
        super().save(*args, **kwargs)
