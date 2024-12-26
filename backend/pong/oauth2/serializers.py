from rest_framework import serializers

from .models import FortyTwoToken


class FortyTwoTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model: type[FortyTwoToken] = FortyTwoToken
        fields: tuple[str, ...] = [
            "id",
            "user",
            "access_token",
            "token_type",
            "access_token_expiry",
            "refresh_token",
            "refresh_token_expiry",
            "scope",
            "created_at",
            "updated_at",
        ]
        # トークン情報はサーバー内でしか管理しないため
        read_only_fields: tuple[str, ...] = [
            # "access_token",
            "token_type",
            "access_token_expiry",
            # "refresh_token",
            "refresh_token_expiry",
            "scope",
            "created_at",
            "updated_at",
        ]
        extra_kwargs: dict = {
            "access_token": {"write_only": True},
            "refresh_token": {"write_only": True},
        }

    def create(self, validated_data: dict) -> FortyTwoToken:
        forty_two_token = FortyTwoToken.objects.create(
            # todo: userを作成
            access_token=validated_data["access_token"],
            token_type=validated_data["token_type"],
            access_token_expiry=validated_data["access_token_expiry"],
            refresh_token=validated_data["refresh_token"],
            refresh_token_expiry=validated_data["refresh_token_expiry"],
            scope=validated_data["scope"],
        )
        return forty_two_token