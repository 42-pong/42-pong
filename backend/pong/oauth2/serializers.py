from django.contrib.auth.models import User
from rest_framework import serializers

from . import models


# todo: create_account関数使用可能になったらUserSerializer削除
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }

    # todo:
    #  - serializer.errorsに複数のエラーメッセージをセット
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

    # OAuth2.0の場合はパスワードは不用。emailは42のリソースサーバーから取得するため必須
    def validate(self, data: dict) -> dict:
        required_fields: list[str] = [
            "username",
            "email",
        ]
        self._validate_required_fields(data, required_fields)
        return data

    def create(self, validated_data: dict) -> User:
        user: User = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password="",
        )
        return user


class OAuth2Serializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model: type[models.OAuth2] = models.OAuth2
        fields: list[str] = [
            "id",
            "user",
            "provider",
            "provider_id",
            "created_at",
            "updated_at",
        ]

        # todo: validate作成

        def create(self, validated_data: dict) -> models.OAuth2:
            oauth2 = models.OAuth2.objects.create(
                # todo: userを作成
                provider=validated_data["provider"],
                provider_id=validated_data["provider_id"],
            )
            return oauth2


class FortyTwoTokenSerializer(serializers.ModelSerializer):
    oauth2 = serializers.PrimaryKeyRelatedField(
        queryset=models.OAuth2.objects.all()
    )

    class Meta:
        model: type[models.FortyTwoToken] = models.FortyTwoToken
        fields: list[str] = [
            "id",
            "oauth2",
            "access_token",
            "token_type",
            "access_token_expiry",
            "refresh_token",
            "refresh_token_expiry",
            "scope",
            "created_at",
            "updated_at",
        ]

        extra_kwargs: dict = {
            "access_token": {"write_only": True},
            "refresh_token": {"write_only": True},
        }

    # todo: validate作成

    def create(self, validated_data: dict) -> models.FortyTwoToken:
        forty_two_token = models.FortyTwoToken.objects.create(
            # todo: oauth2を作成
            access_token=validated_data["access_token"],
            token_type=validated_data["token_type"],
            access_token_expiry=validated_data["access_token_expiry"],
            refresh_token=validated_data["refresh_token"],
            refresh_token_expiry=validated_data["refresh_token_expiry"],
            scope=validated_data["scope"],
        )
        return forty_two_token
