from django.test import TestCase

from ...constants import PlayerFields, UserFields
from ...models import Player
from ...serializers import PlayerSerializer


class PlayerSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.user_data = {
            UserFields.USERNAME: "testuser_1",
            UserFields.EMAIL: "testuser_1@example.com",
            UserFields.PASSWORD: "testpassword",
        }
        # DB追加時に自動でセットされるID,CREATED_AT,UPDATED_ATは省略
        self.player_data = {
            PlayerFields.USER: self.user_data,
        }

    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    def test_player_serializer_valid_data(self) -> None:
        """
        正常なデータが渡された場合にエラーにならないことを確認する
        """
        serializer: PlayerSerializer = PlayerSerializer(data=self.player_data)

        self.assertTrue(serializer.is_valid())

    def test_player_serializer_create(self) -> None:
        """
        PlayerSerializerのcreate()メソッドが正常に動作することを確認する
        """
        serializer: PlayerSerializer = PlayerSerializer(data=self.player_data)
        if not serializer.is_valid():
            # このテストではerrorにならない想定
            raise AssertionError(serializer.errors)
        player: Player = serializer.save()

        # todo: 現在Player独自のfieldがないため、紐づくUserのfieldのみ確認している
        #       今後Player独自のfieldが追加された時にテストも追加する
        self.assertEqual(
            player.user.username, self.user_data[UserFields.USERNAME]
        )
        self.assertEqual(player.user.email, self.user_data[UserFields.EMAIL])

    def test_player_serializer_multi_create(self) -> None:
        """
        PlayerSerializerのcreate()メソッドが複数回呼ばれた場合に正常に動作することを確認する
        """
        # 2人目のアカウント情報
        user_data_2 = {
            UserFields.USERNAME: "testuser_2",
            UserFields.EMAIL: "testuser_2@example.com",
            UserFields.PASSWORD: "testpassword",
        }
        player_data_2 = {
            PlayerFields.USER: user_data_2,
        }

        # 2人共アカウントを作成し,正常に1対1で紐づいているか確認
        for player_data in (self.player_data, player_data_2):
            serializer: PlayerSerializer = PlayerSerializer(data=player_data)
            if not serializer.is_valid():
                # このテストではerrorにならない想定
                raise AssertionError(serializer.errors)
            player: Player = serializer.save()

            # todo: Player独自のfieldが追加された時にテストも追加する
            self.assertEqual(
                player.user.username,
                player_data[PlayerFields.USER][UserFields.USERNAME],
            )
            self.assertEqual(
                player.user.email,
                player_data[PlayerFields.USER][UserFields.EMAIL],
            )

