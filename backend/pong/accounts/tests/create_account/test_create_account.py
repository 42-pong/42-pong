from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from ... import create_account


# test用にUserをmodelに設定したSerializer
class MockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


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

        user: User = create_account_result.unwrap()
        self.assertEqual(user.username, "testuser")
