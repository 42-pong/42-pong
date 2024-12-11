from django.contrib.auth.models import User
from rest_framework import serializers


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

    # serializer.save()の内部で呼ばれる
    def create(self, validated_data: dict) -> User:
        # todo: usernameはBEが自動生成する
        user: User = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
