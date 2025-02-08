import os

from django.contrib.auth.models import User
from django.test import TestCase

from .. import models


# todo: PlayerModelにフィールドが追加された際にテストも追加
class PlayerModelTestCase(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        # User作成
        self.user: User = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )
        # Player作成
        self.player: models.Player = models.Player.objects.create(
            user=self.user
        )
        # tearDown()をスキップするかどうかのフラグ
        self.skip_teardown = False

    def tearDown(self) -> None:
        """
        TestCaseのtearDownメソッドのオーバーライド
        player.delete()でアバター画像を明示的に削除する必要がある
        """
        if self.skip_teardown:
            return
        self.player.delete()

    def test_create_player_and_user(self) -> None:
        """
        PlayerとUserが1つずつ作成されたことを確認
        """
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(models.Player.objects.count(), 1)

    def test_related_user_data(self) -> None:
        """
        作成したPlayerとUserが紐づいていることを確認
        """
        # playerに紐づくuser_idからUserを取得できることを確認
        user_id: int = self.player.user.id
        user: User = User.objects.get(id=user_id)

        # 取得したUserの情報が一致することを確認
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_delete_player(self) -> None:
        """
        Playerを削除し、紐づくUserは削除されないことを確認
        """
        user_id: int = self.player.user.id
        # Player削除
        self.player.delete()
        self.skip_teardown = True

        # Playerが削除されていることを確認
        self.assertEqual(models.Player.objects.count(), 0)
        # Userが削除されていないことを確認
        self.assertTrue(User.objects.filter(id=user_id).exists())

    def test_delete_related_user(self) -> None:
        """
        Playerに紐づくUserを削除すると、UserとPlayerが削除されることを確認
        """
        # User削除
        self.user.delete()

        # UserとPlayerが両方削除されていることを確認
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)

    def test_set_valid_display_name(self) -> None:
        """
        max_length以下の正しいdisplay_nameが指定されている場合、
        Playerのdisplay_nameにその値が設定されていることを確認
        """
        # setUp()とは別のUserを作成
        user: User = User.objects.create_user(
            username="testuser_2",
            email="testuser_2@example.com",
            password="testpassword",
        )
        # Player作成
        player: models.Player = models.Player.objects.create(
            user=user,
            display_name="valid_name",  # 正しいdisplay_name
        )

        self.assertEqual(player.display_name, "valid_name")
        player.delete()

    def test_avatar_file_creation(self) -> None:
        """
        アバター画像が実際に作成されていることを確認
        """
        self.assertTrue(self.player.avatar.name.startswith("avatars/"))
        self.assertTrue(self.player.avatar.name.endswith(".png"))
        self.assertTrue(os.path.exists(self.player.avatar.path))

    def test_avatar_file_deletion(self) -> None:
        """
        Player削除時にアバター画像も削除されていることを確認
        """
        avatar_path: str = self.player.avatar.path
        self.player.delete()
        self.skip_teardown = True

        self.assertFalse(os.path.exists(avatar_path))
