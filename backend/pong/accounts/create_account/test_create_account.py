from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from . import create_account


# test用にUserをmodelに設定したSerializer
class MockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


# todo: validationの実装に合わせてテスト追加
class CreateAccountTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.mock_user_serializer: MockUserSerializer = MockUserSerializer(
            data=self.user_data
        )
        if not self.mock_user_serializer.is_valid():
            # この関数ではerrorにならない想定
            raise AssertionError(self.mock_user_serializer.errors)

    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    def test_create_account_with_valid_user_serializer(self) -> None:
        """
        Userをmodelに設定した有効なUserSerializerを使ってアカウント作成できるかを確認する
        """
        player_data: dict = {}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(
                self.mock_user_serializer, player_data
            )
        )
        self.assertEqual(create_account_result.is_ok, True)

        user_serializer_data: dict = create_account_result.unwrap()
        self.assertEqual(user_serializer_data["username"], "testuser")

    def test_get_unique_random_username_string(self) -> None:
        """
        get_unique_random_username()のユニットテスト
        文字数と、英数字からなるusernameが生成されていることを確認
        """
        random_username: str = create_account.get_unique_random_username()

        self.assertEqual(len(random_username), create_account.USERNAME_LENGTH)
        self.assertTrue(all(char.isalnum() for char in random_username))

    def test_get_unique_random_username_unique(self) -> None:
        """
        get_unique_random_username()のユニットテスト
        生成されたusernameがユニークであることを軽く確認
        """
        for _ in range(5):
            random_username: str = create_account.get_unique_random_username()

            self.assertFalse(
                User.objects.filter(username=random_username).exists()
            )
