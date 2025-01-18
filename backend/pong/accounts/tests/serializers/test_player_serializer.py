from typing import Final

from django.contrib.auth.models import User
from django.test import TestCase

from ... import constants
from ...player import models, serializers

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD
USER: Final[str] = constants.PlayerFields.USER


class PlayerSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.user_data = {
            USERNAME: "testuser_1",
            EMAIL: "testuser_1@example.com",
            PASSWORD: "testpassword",
        }

    def _create_user(self, user_data: dict) -> User:
        """
        Userを作成するヘルパーメソッド
        """
        user: User = User.objects.create_user(**user_data)
        return user

    def _create_player(self, player_data: dict) -> models.Player:
        """
        Playerを作成するヘルパーメソッド
        """
        player_serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=player_data)
        )
        if not player_serializer.is_valid():
            # この関数ではerrorにならない想定
            raise AssertionError(player_serializer.errors)
        player: models.Player = player_serializer.save()
        return player

    def _create_account(self, user_data: dict) -> models.Player:
        """
        Userと紐づくPlayerを作成するヘルパーメソッド
        """
        user: User = self._create_user(user_data)
        player_data: dict = {
            USER: user.id,
        }
        player: models.Player = self._create_player(player_data)
        return player

    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    def test_valid_data(self) -> None:
        """
        正常なデータが渡された場合にエラーにならないことを確認する
        """
        user: models.User = self._create_user(self.user_data)
        player_data: dict = {
            USER: user.id,
        }
        serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=player_data)
        )

        self.assertTrue(serializer.is_valid())

    def test_create(self) -> None:
        """
        PlayerSerializerのcreate()が、正常にPlayerを作成できることを確認する
        """
        player: models.Player = self._create_account(self.user_data)

        # todo: 現在Player独自のfieldがないため、紐づくUserのfieldのみ確認している
        #       今後Player独自のfieldが追加された時にテストも追加する
        self.assertEqual(player.user.username, self.user_data[USERNAME])
        self.assertEqual(player.user.email, self.user_data[EMAIL])

    def test_multi_create(self) -> None:
        """
        PlayerSerializerのcreate()メソッドが複数回呼ばれた場合に、
        正常に全てのPlayerが作成されることを確認する
        """
        # 2人目のアカウント情報
        user_data_2: dict = {
            USERNAME: "testuser_2",
            EMAIL: "testuser_2@example.com",
            PASSWORD: "testpassword",
        }

        # 2人共アカウントを作成し,UserとPlayerが正常に1対1で紐づいているか確認
        for user_data in (self.user_data, user_data_2):
            player: models.Player = self._create_account(user_data)

            # todo: Player独自のfieldが追加された時にテストも追加する
            self.assertEqual(
                player.user.username,
                user_data[USERNAME],
            )
            self.assertEqual(
                player.user.email,
                user_data[EMAIL],
            )

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    # todo: PlayerSerializer独自のバリデーションが追加された場合にテストを追加する
