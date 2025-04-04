import dataclasses
from typing import Final
from unittest import mock

from django.contrib.auth.models import User
from django.db import DatabaseError
from django.test import TestCase
from rest_framework import serializers

from ..player import models
from . import create_account

MOCK_AVATAR_NAME: Final[str] = "avatars/test.png"


@dataclasses.dataclass(frozen=True)
class MockUserField:
    username: str = "username"
    password: str = "password"


# todo: 正常ケースもunittest.mockに置き換えられたら置き換える
# test用にUserをmodelに設定したSerializer
class MockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            MockUserField.username,
            MockUserField.password,
        )


# todo: validationの実装に合わせてテスト追加
class CreateAccountTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.user_data = {
            MockUserField.username: "testuser",
            MockUserField.password: "testpassword",
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
    @mock.patch(
        "accounts.player.identicon.generate_identicon",
        return_value=MOCK_AVATAR_NAME,
    )
    def test_create_account_with_valid_user_serializer(
        self, mock_identicon: mock.MagicMock
    ) -> None:
        """
        Userをmodelに設定した有効なUserSerializerを使ってアカウント作成できるかを確認する
        """
        player_data: dict = {}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(
                self.mock_user_serializer, player_data
            )
        )
        self.assertTrue(create_account_result.is_ok)

        user_serializer_data: dict = create_account_result.unwrap()
        self.assertEqual(
            user_serializer_data[MockUserField.username], "testuser"
        )

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

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    @mock.patch("accounts.user.serializers.UserSerializer")
    def test_transaction_rollback_on_user_save_failure(
        self, mock_user_serializer: mock.Mock
    ) -> None:
        """
        Userの保存に失敗した場合にトランザクションがロールバックされ、
        UserとPlayerが保存されていないことを確認
        """
        # userの保存に失敗するuser_serializerのmockを用意
        mock_user_serializer.Meta.model = User
        mock_user_serializer.save.side_effect = DatabaseError(
            "Failed to save user"
        )
        # account作成
        player_data: dict = {}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(mock_user_serializer, player_data)
        )

        self.assertFalse(create_account_result.is_ok)
        self.assertIn("DatabaseError", create_account_result.unwrap_error())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)

    @mock.patch("accounts.create_account.create_account._save_player")
    def test_transaction_rollback_on_player_save_failure(
        self, mock_save_player: mock.Mock
    ) -> None:
        """
        Userは正しく保存されるが、Playerの保存に失敗した場合にトランザクションがロールバックされ、
        UserとPlayerが保存されていないことを確認
        """
        # Playerの保存に失敗する_save_player()のmockを用意
        mock_save_player.side_effect = DatabaseError("Failed to save player")
        # account作成
        player_data: dict = {}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(
                self.mock_user_serializer, player_data
            )
        )

        self.assertFalse(create_account_result.is_ok)
        self.assertIn("DatabaseError", create_account_result.unwrap_error())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)

    @mock.patch("accounts.user.serializers.UserSerializer")
    def test_transaction_rollback_on_user_validation_failure(
        self, mock_user_serializer: mock.Mock
    ) -> None:
        """
        Userのバリデーションに失敗した場合にトランザクションがロールバックされ、
        UserとPlayerが保存されていないことを確認
        """
        # userのバリデーションに失敗するuser_serializerのmockを用意
        mock_user_serializer.Meta.model = User
        mock_user_serializer.is_valid.side_effect = (
            serializers.ValidationError(
                {"username": ["This field is required."]}
            )
        )
        # account作成
        player_data: dict = {}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(mock_user_serializer, player_data)
        )

        self.assertFalse(create_account_result.is_ok)
        self.assertIn("username", create_account_result.unwrap_error())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)

    @mock.patch("accounts.create_account.create_account._save_player")
    def test_transaction_rollback_on_player_validation_failure(
        self, mock_save_player: mock.Mock
    ) -> None:
        """
        Playerのバリデーションに失敗した場合にトランザクションがロールバックされ、
        UserとPlayerが保存されていないことを確認
        """
        # Playerのバリデーションに失敗する_save_player()のmockを用意
        mock_save_player.side_effect = serializers.ValidationError(
            {"display_name": ["This field is required."]}
        )
        # account作成
        player_data: dict = {}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(
                self.mock_user_serializer, player_data
            )
        )

        self.assertFalse(create_account_result.is_ok)
        self.assertIn("display_name", create_account_result.unwrap_error())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)
