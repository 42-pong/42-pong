from django.contrib.auth.models import User
from rest_framework import serializers

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
        """
        # todo: usernameはBEが自動生成する
        user: User = User.objects.create_user(
            username=validated_data[constants.UserFields.USERNAME],
            email=validated_data[constants.UserFields.EMAIL],
            password=validated_data[constants.UserFields.PASSWORD],
        )
        return user


class PlayerSerializer(serializers.ModelSerializer):
    """
    Playerモデルのシリアライザ
    Playerモデルの作成・バリデーションを行う
    """

    # 同じ変数名(user)をfieldsに指定する必要がある
    user: UserSerializer = UserSerializer()

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

    # todo: Playerモデルにfieldが追加されたらvalidate()を作成する

    # AccountCreateViewのserializer.save()の内部で呼ばれる
    # todo: 多分トランザクションの処理が必要。User,Playerのどちらかが作成されなかった場合はロールバック
    def create(self, validated_data: dict) -> models.Player:
        """
        新規Playerを作成する
        UserSerializerを使用してUserを作成し、そのUserと関連付けたPlayerを作成する
        """
        # requestの中にuserがあるので、それだけpopしてUserSerializerに渡す
        user_data: dict = validated_data.pop(constants.PlayerFields.USER)
        user_serializer: UserSerializer = UserSerializer(data=user_data)

        # UserSerializerのvalidate()が成功したらUserを作成する
        user_serializer.is_valid(raise_exception=True)
        new_user: User = user_serializer.save()

        # Userを作成した後でPlayerを作成する
        player: models.Player = models.Player.objects.create(user=new_user)
        return player
