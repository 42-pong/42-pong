from django.contrib.auth.models import User
from django.db import models


class TwoFactorAuth(models.Model):
    # 1対1 / 認証サービスごとに別のアカウントを作成するため
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="two_fa"
    )
    is_done_2fa = models.BooleanField(default=False)
    secret = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = "two_factor_auth"

    def __str__(self) -> str:
        return f"user: {self.user.username}, is_done_2fa: {self.is_done_2fa}"
