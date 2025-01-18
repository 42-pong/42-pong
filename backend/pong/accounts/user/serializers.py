from django.contrib.auth.models import User
from rest_framework import serializers, validators

from .. import constants


class UserSerializer(serializers.ModelSerializer):
    """
    Userモデルのシリアライザ
    Userモデルの作成・バリデーションを行う
    """

    # EmailField: デフォルトがrequired=True, allow_blank=False
    # todo: max_length、min_lengthの設定
    email = serializers.EmailField(
        # UniqueValidator: emailをユニークにする
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            constants.UserFields.ID,
            constants.UserFields.USERNAME,
            constants.UserFields.EMAIL,
            constants.UserFields.PASSWORD,
        )
        extra_kwargs = {
            constants.UserFields.PASSWORD: {"write_only": True},
        }

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
