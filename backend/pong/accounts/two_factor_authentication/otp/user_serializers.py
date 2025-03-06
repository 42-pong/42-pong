from django.contrib.auth.models import User
from rest_framework import serializers

from ... import constants
from ...create_account import create_account


class UserSerializer(serializers.ModelSerializer):
    """
    2FAを通してアカウントを作成する際に使用するUser用のシリアライザ
    passwordが既にhash化されているものが渡されるためそのまま保存する必要がある
    """

    username = serializers.CharField(max_length=10, required=False)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            constants.UserFields.ID,
            constants.UserFields.USERNAME,
            constants.UserFields.EMAIL,
            constants.UserFields.PASSWORD,
        )
        extra_kwargs = {
            constants.UserFields.USERNAME: {"read_only": True},
            constants.UserFields.PASSWORD: {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        """
        2FAを通してアカウントを新規作成するcreate()のオーバーライド
        """
        # usernameはランダム生成
        username: str = create_account.get_unique_random_username()
        email: str = validated_data[constants.UserFields.EMAIL]
        # User作成(create_user()を使うとpasswordがhash化されてしまうため、create()を使う)
        user: User = User.objects.create(username=username, email=email)

        password: str = validated_data[constants.UserFields.PASSWORD]
        # passwordはOTP発行時に既にhash化されているため、そのまま保存する必要がある
        user.password = password
        user.save()
        return user
