from django.db.models import EmailField, Model, TextField


class TemporaryUser(Model):
    """
    sign upをしてからワンタイムパスワードの承認するまでの一時的なユーザーモデル
    """

    email = EmailField(unique=True)
    # ハッシュ化されたパスワードを保存するためTextFieldを使用
    password = TextField()

    class Meta:
        db_table = "temporary_users"

    def save(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """
        TemporaryUserインスタンスを保存する際のsave()のオーバーライド
        """
        super().save(*args, **kwargs)
