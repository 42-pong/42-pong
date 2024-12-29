from typing import Final

from django.contrib.auth.models import User
from django.test import TestCase

from ... import constants, models, serializers

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
        self.user = User.objects.create_user(**self.user_data)
        # DB追加時に自動でセットされるID,CREATED_AT,UPDATED_ATは省略
        self.player_data = {
            USER: self.user.id,
        }

    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    def test_player_serializer_valid_data(self) -> None:
        """
        正常なデータが渡された場合にエラーにならないことを確認する
        """
        serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=self.player_data)
        )

        self.assertTrue(serializer.is_valid())

    def test_player_serializer_create(self) -> None:
        """
        PlayerSerializerのcreate()メソッドが正常に動作することを確認する
        """
        serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=self.player_data)
        )
        if not serializer.is_valid():
            # このテストではerrorにならない想定
            raise AssertionError(serializer.errors)
        player: models.Player = serializer.save()

        # todo: 現在Player独自のfieldがないため、紐づくUserのfieldのみ確認している
        #       今後Player独自のfieldが追加された時にテストも追加する
        self.assertEqual(player.user.username, self.user_data[USERNAME])
        self.assertEqual(player.user.email, self.user_data[EMAIL])

    def test_player_serializer_multi_create(self) -> None:
        """
        PlayerSerializerのcreate()メソッドが複数回呼ばれた場合に正常に動作することを確認する
        """
        # 2人目のアカウント情報
        user_data_2: dict = {
            USERNAME: "testuser_2",
            EMAIL: "testuser_2@example.com",
            PASSWORD: "testpassword",
        }
        user_2: User = User.objects.create_user(**user_data_2)
        player_data_2: dict = {
            USER: user_2.id,
        }

        # 2人共アカウントを作成し,正常に1対1で紐づいているか確認
        for user_data, player_data in (
            (self.user_data, self.player_data),
            (user_data_2, player_data_2),
        ):
            serializer: serializers.PlayerSerializer = (
                serializers.PlayerSerializer(data=player_data)
            )
            if not serializer.is_valid():
                # このテストではerrorにならない想定
                raise AssertionError(serializer.errors)
            player: models.Player = serializer.save()

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
