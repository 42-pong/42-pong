from django.contrib.auth.models import User
from rest_framework import serializers

from . import models


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
            "email": {"required": True},
            "password": {"write_only": True, "allow_blank": True},
        }

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

    # todo: より詳細なvalidationの実装
    def validate(self, data: dict) -> dict:
        return data


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

    def _validate_token_type(self, data: dict) -> None:
        """
        トークンタイプが有効な値であるかを検証する関数。

        Args:
            data (dict): トークン情報を含む辞書。`token_type`キーを必須で含む。

        Raises:
            serializers.ValidationError: `token_type`が有効な値でない場合
        """
        valid_token_types = ["bearer", "mac"]
        if data["token_type"] not in valid_token_types:
            raise serializers.ValidationError(
                {
                    "token_type": f"Invalid token_type. Must be one of {valid_token_types}."
                }
            )

    # todo: より詳細なvalidationの実装
    def validate(self, data: dict) -> dict:
        self._validate_token_type(data)
        return data
