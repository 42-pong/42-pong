from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from .. import constants


class UserSerializer(serializers.ModelSerializer):
    """
    Userモデルのシリアライザ
    Userモデルの作成・バリデーションを行う
    """

    # EmailField: デフォルトがrequired=True, allow_blank=False
    # EmailValidator: EmailFieldがデフォルトで使用しているバリデーター
    #   - emailの形式チェック
    #   - max_length=320
    email = serializers.EmailField(
        validators=[
            # emailをユニークにする
            validators.UniqueValidator(queryset=User.objects.all()),
        ]
    )
    # validate_password: 4つのvalidatorでチェックされる
    # https://docs.djangoproject.com/ja/5.1/topics/auth/passwords/#included-validators
    password = serializers.CharField(
        write_only=True,
        max_length=50,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = (
            constants.UserFields.ID,
            constants.UserFields.USERNAME,
            constants.UserFields.EMAIL,
            constants.UserFields.PASSWORD,
        )

    # PlayerSerializerのuser_serializer.save()の内部で呼ばれる
    def create(self, validated_data: dict) -> User:
        """
        新規Userを作成する
        create_user(): emailのnormalize、passwordのhash化などを自動で行う

        Args:
            validated_data: バリデーション後の全てのuser fieldが含まれるdict

        Returns:
            User: 新規作成しDBに追加されたUser
        """
        user: User = User.objects.create_user(**validated_data)
        return user
