from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Player


# PlayerSerializerが呼ばれる時にこのUserSerializerも呼ばれる
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: type[User] = User
        fields: tuple[str, ...] = (
            "id",
            "username",
            "email",
            "password",
        )
        extra_kwargs: dict = {
            "password": {"write_only": True},
        }

    # 必須なフィールドが空の場合はエラー
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
        required_fields: list[str] = ["username", "email", "password"]
        self._validate_required_fields(data, required_fields)
        return data

    # PlayerSerializerのuser_serializer.save()の内部で呼ばれる
    def create(self, validated_data: dict) -> User:
        # todo: usernameはBEが自動生成する
        user: User = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class PlayerSerializer(serializers.ModelSerializer):
    # 同じ変数名(user)をfieldsに指定する必要がある
    user: UserSerializer = UserSerializer()

    class Meta:
        model: type[Player] = Player
        fields: tuple[str, ...] = ("id", "user", "created_at", "updated_at")
        extra_kwargs: dict = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    # todo: Playerモデルにfieldが追加されたらvalidate()を作成する

    # AccountCreateViewのserializer.save()の内部で呼ばれる
    # todo: 多分トランザクションの処理が必要。User,Playerのどちらかが作成されなかった場合はロールバック
    def create(self, validated_data: dict) -> Player:
        # requestの中にuserがあるので、それだけpopしてUserSerializerに渡す
        user_data: dict = validated_data.pop("user")
        user_serializer: UserSerializer = UserSerializer(data=user_data)

        # UserSerializerのvalidate()が成功したらUserを作成する
        user_serializer.is_valid(raise_exception=True)
        new_user: User = user_serializer.save()

        # Userを作成した後でPlayerを作成する
        player: Player = Player.objects.create(user=new_user)
        return player
