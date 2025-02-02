from typing import Final

from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.test import TestCase

from accounts import constants
from accounts.player import models

from ... import serializers

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD
USER: Final[str] = constants.PlayerFields.USER


class UsersSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        2つのUserと、そのUserに紐づく2つのPlayerをDBに保存
        """

        def _create_user_and_related_player(user_data: dict) -> User:
            user: User = User.objects.create_user(**user_data)
            player_data: dict = {
                USER: user,
            }
            models.Player.objects.create(**player_data)
            return user

        self.user_data_1: dict = {
            USERNAME: "testuser_1",
            EMAIL: "testuser_1@example.com",
            PASSWORD: "testpassword",
        }
        self.user_data_2: dict = {
            USERNAME: "testuser_2",
            EMAIL: "testuser_2@example.com",
            PASSWORD: "testpassword",
        }
        self.user_1: User = _create_user_and_related_player(self.user_data_1)
        self.user_2: User = _create_user_and_related_player(self.user_data_2)

    def test_valid_multiple_instance(self) -> None:
        """
        正常なインスタンスが複数渡された場合に、dataにインスタンス分の値が入っていることを確認
        """
        # Userに紐づくPlayer全てのQuerySetを取得
        all_players_with_users: QuerySet[models.Player] = (
            models.Player.objects.select_related(USER).all()
        )
        # serializer作成
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            all_players_with_users, many=True
        )

        # シリアライズ済みdataからusernameのみのlistを作成
        serializer_data_usernames: list[str] = [
            data[USERNAME] for data in serializer.data
        ]
        self.assertEqual(len(serializer.data), 2)
        for username in (
            self.user_data_1[USERNAME],
            self.user_data_2[USERNAME],
        ):
            self.assertIn(username, serializer_data_usernames)
            # todo: display_nameも確認する

    def test_non_users(self) -> None:
        """
        ユーザーが存在しない場合に、エラーにならずdataが空であることを確認
        """
        # User,紐づくPlayerを全て削除
        User.objects.all().delete()

        all_players_with_users: QuerySet[models.Player] = (
            models.Player.objects.select_related(USER).all()
        )
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            all_players_with_users, many=True
        )

        self.assertEqual(serializer.data, [])
