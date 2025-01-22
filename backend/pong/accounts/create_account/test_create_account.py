import dataclasses
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from ..player import models
from . import create_account


@dataclasses.dataclass(frozen=True)
class MockUserField:
    username: str = "username"
    password: str = "password"


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
    def test_transaction_fail_to_save_user(self) -> None:
        """
        Userの保存に失敗した場合にトランザクションがロールバックされ、
        UserとPlayerが保存されていないことを確認
        """
        # userの保存に失敗するuser_serializerを用意
        self.user_data[MockUserField.password] = ""  # passwordが空だとエラー
        mock_user_serializer: MockUserSerializer = MockUserSerializer(
            data=self.user_data
        )
        # account作成
        player_data: dict = {}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(mock_user_serializer, player_data)
        )

        self.assertFalse(create_account_result.is_ok)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)

    # todo: 実装されたらskipを外す
    @unittest.skip("display_nameがplayerフィールドに追加されたら通るテスト")
    def test_transaction_fail_to_save_player(self) -> None:
        """
        Userは正しく保存されるが、Playerの保存に失敗した場合にトランザクションがロールバックされ、
        UserとPlayerが保存されていないことを確認
        """
        # Playerの保存に失敗するplayer_dataを用意してaccount作成
        player_data: dict = {"display_name": "over-15-characters"}
        create_account_result: create_account.CreateAccountResult = (
            create_account.create_account(
                self.mock_user_serializer, player_data
            )
        )

        self.assertFalse(create_account_result.is_ok)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)
