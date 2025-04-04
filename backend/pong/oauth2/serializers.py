from django.contrib.auth.models import User
from rest_framework import serializers

from . import models


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
    # - OAuth2Serializerのvalidate関数で42以外のプロバイダーを弾く関数を作成する
    # - 同じproviderの場合はprovider_id が既に存在するかかどうか検証
    def validate(self, data: dict) -> dict:
        return data


# todo: provider/serialzier.py移動する
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

    def _validate_token_type(self, token_type: str) -> None:
        """
        トークンタイプが有効な値であるかを検証する関数。

        Args:
            token_type (str): トークンタイプ

        Raises:
            serializers.ValidationError: `token_type`が有効な値でない場合
        """
        valid_token_types = ["bearer", "mac"]
        if token_type not in valid_token_types:
            raise serializers.ValidationError(
                {
                    "token_type": f"Invalid token_type. Must be one of {valid_token_types}."
                }
            )

    # todo: より詳細なvalidationの実装
    def validate(self, data: dict) -> dict:
        self._validate_token_type(data["token_type"])
        return data
