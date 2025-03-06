from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    Model,
    OneToOneField,
)

from ..temporary_user.models import TemporaryUser


class OTP(Model):
    """
    OTP(One-Time Password)モデル
    TemporaryUserに紐づけて、OTP確認用のコードを一時的に保存する
    """

    temp_user = OneToOneField(
        TemporaryUser, on_delete=CASCADE, related_name="otp"
    )
    otp_code = CharField(max_length=6)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otps"

    def save(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """
        OTPインスタンスを保存する際のsave()のオーバーライド
        """
        super().save(*args, **kwargs)
