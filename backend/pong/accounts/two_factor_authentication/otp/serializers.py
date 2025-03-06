from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from ..otp import constants as otp_constants
from ..temporary_user import models as temporary_user_models
from . import constants, models


class OTPSerializer(serializers.Serializer):
    """
    OTPの検証を行うシリアライザ
    """

    temp_user: serializers.PrimaryKeyRelatedField[
        temporary_user_models.TemporaryUser
    ] = serializers.PrimaryKeyRelatedField(
        queryset=temporary_user_models.TemporaryUser.objects.all()
    )
    otp_code = serializers.CharField(max_length=constants.OPT_CODE_LENGTH)

    class Meta:
        model = models.OTP
        fields = (
            constants.OptFields.TEMP_USER,
            constants.OptFields.OTP_CODE,
        )

    def validate(self, data: dict) -> dict:
        """
        validate()のオーバーライド
        requestのOTPの検証を行う
        - 有効期限のチェック
        - DBに保存されているOPTとの一致をチェック
        """
        temp_user_id: int = data[otp_constants.OptFields.TEMP_USER]
        request_otp: str = data[otp_constants.OptFields.OTP_CODE]

        try:
            otp_obj: models.OTP = models.OTP.objects.get(
                temp_user_id=temp_user_id
            )
        except models.OTP.DoesNotExist:
            # そのemailに対してOTPを発行していない場合
            raise serializers.ValidationError(
                {
                    otp_constants.OptFields.OTP_CODE: "No OTP issued for this email"
                }
            )

        # OTPの有効期限をチェック(5分間有効)
        if timezone.now() > otp_obj.created_at + timedelta(
            minutes=constants.EXPIRED_MINUTES
        ):
            raise serializers.ValidationError(
                {otp_constants.OptFields.OTP_CODE: "OTP has expired"}
            )

        # OTPコードの一致をチェック
        if request_otp != otp_obj.otp_code:
            raise serializers.ValidationError(
                {otp_constants.OptFields.OTP_CODE: "Invalid OTP"}
            )

        return data
