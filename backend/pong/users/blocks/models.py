from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from . import constants


class BlockRelationship(models.Model):
    """
    ブロック関係を表すモデル
    user: ブロックする側のユーザー
    blocked_user: ブロックされる側のユーザー
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="block_relationships",
        db_column=constants.BlockRelationshipFields.USER_ID,
    )
    blocked_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocked_by",
        db_column=constants.BlockRelationshipFields.BLOCKED_USER_ID,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "block_relationships"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "blocked_user"],
                name="unique_block_relationship",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} block {self.blocked_user.username}"

    def clean(self) -> None:
        """
        save()される前にバリデーションを行うclean()のオーバーライド
        """
        # 自分自身をブロックしようとした場合はエラー
        if self.user == self.blocked_user:
            raise ValidationError("You cannot block yourself.")
        super().clean()

    # args,kwargsは型ヒントが複雑かつそのままsuper()に渡したいためignoreで対処
    def save(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """
        save()のオーバーライド
        保存する前にcleanメソッドを明示的に呼び出す必要がある
        """
        self.full_clean()
        super().save(*args, **kwargs)
