from django.contrib.auth.models import User
from rest_framework import relations, serializers

from . import constants, models


class UserSerializer(serializers.ModelSerializer):
    """
    Userモデルのシリアライザ
    Userモデルの作成・バリデーションを行う
    PlayerSerializerが呼ばれると、このUserSerializerも呼ばれる
    """

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

    # todo:
    #  - serializer.errorsに複数のエラーメッセージをセットできそう
    #  - より詳細なvalidationの実装
    def _validate_required_fields(
        self, data: dict, required_fields: list[str]
    ) -> None:
        for field in required_fields:
            # 実装上のミスでdataに存在しないfieldが渡された場合
            if field not in data:
                raise AssertionError(
                    f"{field} is required but not provided in data."
                )
            # dataの中のfieldが空の場合
            if not data.get(field):
                raise serializers.ValidationError(
                    {field: "This field is required."}
                )

    # PlayerSerializerのuser_serializer.is_valid()の内部で呼ばれる
    def validate(self, data: dict) -> dict:
        """
        バリデーションを行う
        - 必須fieldが空の場合はエラーを発生させる
        """
        required_fields: list[str] = [
            constants.UserFields.USERNAME,
            constants.UserFields.EMAIL,
            constants.UserFields.PASSWORD,
        ]
        self._validate_required_fields(data, required_fields)
        return data

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


class PlayerSerializer(serializers.ModelSerializer):
    """
    Playerモデルのシリアライザ
    Playerモデルの作成・バリデーションを行う
    """

    # PrimaryKeyRelatedField: 紐づくターゲットをそのPKを使用して表現する
    # 同じ変数名(user)をfieldsに指定する必要がある
    user: relations.PrimaryKeyRelatedField[User] = (
        relations.PrimaryKeyRelatedField(queryset=User.objects.all())
    )

    class Meta:
        model = models.Player
        fields = (
            constants.PlayerFields.USER,
            constants.PlayerFields.CREATED_AT,
            constants.PlayerFields.UPDATED_AT,
        )
        extra_kwargs = {
            constants.PlayerFields.CREATED_AT: {"read_only": True},
            constants.PlayerFields.UPDATED_AT: {"read_only": True},
        }

    # todo: Playerモデルにfieldが追加されたらvalidate(),create()を作成する
