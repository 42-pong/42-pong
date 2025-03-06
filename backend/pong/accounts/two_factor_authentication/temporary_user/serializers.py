from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, UserManager
from rest_framework import serializers

from ... import constants
from ...user import serializers as user_serializers
from . import models


class TemporaryUserSerializer(serializers.ModelSerializer):
    """
    TemporaryUser情報をシリアライズする
    """

    email = serializers.EmailField()
    # 既存のUserSerializerのバリデーションを使用
    password = user_serializers.UserSerializer().fields[
        constants.UserFields.PASSWORD
    ]

    class Meta:
        model = models.TemporaryUser
        fields = (
            constants.UserFields.EMAIL,
            constants.UserFields.PASSWORD,
        )

    def validate(self, data: dict) -> dict:
        """
        validate()のオーバーライド
        """
        email: str = data[constants.UserFields.EMAIL]
        # create_userを使わずUser作成をするので手動で正規化
        email = UserManager.normalize_email(email)

        # 既にアカウントが存在する場合はエラー
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {constants.UserFields.EMAIL: "Account already exists"}
            )
        return data

    def create(self, validated_data: dict) -> models.TemporaryUser:
        email: str = validated_data[constants.UserFields.EMAIL]
        password: str = validated_data[constants.UserFields.PASSWORD]

        # 既にTemporaryUserに存在する場合は削除してから新規作成
        # todo: update()で良かったかも
        models.TemporaryUser.objects.filter(email=email).delete()

        # パスワードをハッシュ化
        validated_data[constants.UserFields.PASSWORD] = make_password(password)

        return super().create(validated_data)
