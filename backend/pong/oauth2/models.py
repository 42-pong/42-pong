from django.contrib.auth.models import User
from django.db import models


class OAuth2(models.Model):
    # 1対1 / 認証サービスごとに別のアカウントを作成するため
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="oauth2"
    )
    provider = models.CharField(max_length=255)
    provider_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "oauth2"

    def __str__(self) -> str:
        return self.provider


class FortyTwoToken(models.Model):
    user = models.OneToOneField(
        OAuth2, on_delete=models.CASCADE, related_name="forty_two_token"
    )
    access_token = models.CharField(max_length=255, unique=True)
    # 42はbearerとmacのみなので6文字で固定
    token_type = models.CharField(max_length=6)
    access_token_expiry = models.DateTimeField()
    refresh_token = models.CharField(max_length=255, unique=True)
    refresh_token_expiry = models.DateTimeField()
    scope = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "forty_two_tokens"

    def __str__(self) -> str:
        return self.access_token
