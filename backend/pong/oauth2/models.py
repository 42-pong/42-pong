from django.contrib.auth.models import User
from django.db import models


class Token(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="token"
    )
    access_token = models.CharField(max_length=255, unique=True)
    # bearerのみなので6文字で固定
    token_type = models.CharField(max_length=6)
    access_token_expiry = models.DateTimeField()
    refresh_token = models.CharField(max_length=255, unique=True)
    refresh_token_expiry = models.DateTimeField()
    scope = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tokens"

    def __str__(self) -> str:
        return self.access_token