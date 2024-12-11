from django.contrib.auth.models import User
from django.db import models


# todo: 表示名・アバター画像PATHなどがfieldに追加される予定
class Player(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="player"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"  # ユーザーが認証に使用するfield

    class Meta:
        db_table = "players"

    def __str__(self) -> str:
        return self.user.username
