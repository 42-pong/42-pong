from django.test import TestCase

from ...constants import PlayerFields, UserFields
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
