from typing import Final

from django.test import TestCase

from oauth2 import models, serializers

REQUIRED: Final[str] = "required"
UNIQUE: Final[str] = "unique"
NULL: Final[str] = "null"


class UserSerializerTestCase(TestCase):
    def setUp(self) -> None:
        """
        unittest.TestCaseのsetUpメソッドをオーバーライドして、テスト実行前に必要な初期設定を行う関数

        初期設定
        - self.SerializerにUserSerializerのインスタンスを代入
        """
        self.Serializer = serializers.UserSerializer

    # todo: パスワードに文字列を入力した場合のテストを書く?（現状だとパスワードの値は入る）
    #       その場合は関数名を変更する。
    def test_valid_serializer(self) -> None:
        """
        正しいデータの場合、正しく機能するかを確認するテスト
        """

        # passwordが空文字を想定
        user_data: dict = {
            "id": 1,
            "username": "pong",
            "email": "pong@gmail.com",
            "password": "",
        }
        serializer: serializers.UserSerializer = self.Serializer(
            data=user_data
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data,
            {"username": "pong", "email": "pong@gmail.com", "password": ""},
        )
        self.assertEqual(
            serializer.data, {"username": "pong", "email": "pong@gmail.com"}
        )
        self.assertTrue(serializer.errors == {})

    def test_serializer_with_missing_required_field(self) -> None:
        """
        必須フィールドが存在しない場合、期待通りにエラーを返すかを確認するテスト
        """
        missing_required_fields_data: dict = {"username": "pong"}
        expected_fields: list[str] = [
            # "username",
            "email",
            "password",
        ]
        serializer: serializers.UserSerializer = self.Serializer(
            data=missing_required_fields_data
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.data, {"username": "pong"})
        for key in expected_fields:
            self.assertEqual(serializer.errors[key][0].code, REQUIRED)

    def test_validate_empty_data(self) -> None:
        """
        空のデータの場合、期待通りにエラーを返すかを確認するテスト
        """
        empty_data: dict = {}
        expected_fields: list[str] = [
            "username",
            "email",
            "password",
        ]
        serializer: serializers.UserSerializer = self.Serializer(
            data=empty_data
        )
        self.assertFalse(serializer.is_valid())
        for key in expected_fields:
            self.assertEqual(serializer.errors[key][0].code, REQUIRED)

    def test_validate_none_data(self) -> None:
        """
        Noneの場合、期待通りにエラーを返すかを確認するテスト
        """
        serializer: serializers.UserSerializer = self.Serializer(data=None)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["non_field_errors"][0].code, NULL)

    # todo: invalidなserializerのテストを書く


class OAuth2SerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = models.User.objects.create_user(
            username="pong", email="pong@example.com", password=""
        )
        self.Serializer = serializers.OAuth2Serializer

    def test_valid_serializer(self) -> None:
        """
        正しいデータの場合、正しく機能するかを確認するテスト
        """
        oauth2_data: dict = {
            "id": 1,
            "user": self.user.id,
            "provider": "42",
            "provider_id": "12345",
        }
        serializer: serializers.OAuth2Serializer = self.Serializer(
            data=oauth2_data
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data,
            {
                "user": self.user,
                "provider": "42",
                "provider_id": "12345",
            },
        )
        self.assertEqual(
            serializer.data,
            {
                "user": self.user.id,
                "provider": "42",
                "provider_id": "12345",
            },
        )
        self.assertTrue(serializer.errors == {})

    def test_validate_unique_provider_id(self) -> None:
        """
        provider と provider_id の組み合わせが既に存在する場合、適切なエラーを返すか確認するテスト
        """
        oauth2: models.OAuth2 = models.OAuth2.objects.create(
            user=self.user, provider="42", provider_id="12345"
        )
        duplicate_data: dict = {
            "user": oauth2.user.id,
            "provider": "42",
            "provider_id": "12345",
        }

        serializer = self.Serializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["provider_id"][0].code, UNIQUE)

    def test_serializer_with_missing_required_field(self) -> None:
        """
        必須フィールドが存在しない場合、期待通りにエラーを返すかを確認するテスト
        """
        missing_required_fields_data: dict = {"provider": "42"}
        serializer: serializers.OAuth2Serializer = self.Serializer(
            data=missing_required_fields_data
        )
        expected_fields: list[str] = [
            "user",
            # "provider",
            "provider_id",
        ]
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        for key in expected_fields:
            self.assertEqual(serializer.errors[key][0].code, REQUIRED)

    def test_validate_empty_data(self) -> None:
        """
        空のデータの場合、期待通りにエラーを返すかを確認するテスト
        """
        empty_data: dict = {}
        serializer = self.Serializer(data=empty_data)
        self.assertFalse(serializer.is_valid())
        expected_fields: list[str] = ["user", "provider", "provider_id"]
        for key in expected_fields:
            self.assertEqual(serializer.errors[key][0].code, REQUIRED)

    def test_validate_none_data(self) -> None:
        """
        Noneの場合、期待通りにエラーを返すかを確認するテスト
        """
        serializer = self.Serializer(data=None)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["non_field_errors"][0].code, NULL)

    # todo: invalidなserializerのテストを書く


class FortyTwoTokenSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user: models.User = models.User.objects.create_user(
            username="pong", email="pong@example.com", password=""
        )
        self.oauth2: models.OAuth2 = models.OAuth2.objects.create(
            user=self.user, provider="42", provider_id="12345"
        )
        self.Serializer = serializers.FortyTwoTokenSerializer

    def test_valid_serializer(self) -> None:
        """
        正しいデータの場合、FortyTwoTokenSerializerが正しく機能するかを確認するテスト
        """
        # todo: 本来アクセサトークンとリフレッシュトークンの値はランダムのためよそれ用のテストする必要あるかも
        token_data: dict = {
            "oauth2": self.oauth2.id,
            "access_token": "valid_access_token",
            "access_token_expiry": "2025-01-01T00:00:00Z",
            "token_type": "bearer",
            "refresh_token": "valid_refresh_token",
            "refresh_token_expiry": "2025-01-01T00:00:00Z",
            "scope": "public",
        }
        serializer = self.Serializer(data=token_data)
        # todo: datetimeについてのテストは時間がかかりそうなため後で書く
        #       - access_token_expiry
        #       - refresh_token_expiry
        expected_data: dict = {
            "oauth2": self.oauth2,
            "access_token": "valid_access_token",
            "token_type": "bearer",
            "refresh_token": "valid_refresh_token",
            "scope": "public",
        }
        self.assertTrue(serializer.is_valid())
        for key, expected_value in expected_data.items():
            self.assertEqual(serializer.validated_data[key], expected_value)
        for key in ["token_type", "scope"]:
            self.assertEqual(serializer.data[key], expected_data[key])
        for key in ["access_token", "refresh_token"]:
            self.assertNotIn(key, serializer.data)

    def test_serializer_with_missing_required_field(self) -> None:
        """
        一部の必須フィールドが存在しない場合、期待通りにエラーを返すかを確認するテスト
        """
        missing_required_fields_data: dict = {"scope": "public"}
        expected_fields: list[str] = [
            "oauth2",
            "access_token",
            "token_type",
            "access_token_expiry",
            "refresh_token",
            "refresh_token_expiry",
            # "scope",
        ]
        serializer: serializers.FortyTwoTokenSerializer = self.Serializer(
            data=missing_required_fields_data
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.data, {"scope": "public"})
        for key in expected_fields:
            self.assertEqual(serializer.errors[key][0].code, REQUIRED)

    def test_validate_empty_data(self) -> None:
        """
        空のデータの場合（全部の必須フィールドが存在しない場合）、期待通りにエラーを返すかを確認するテスト
        """
        empty_data: dict = {}
        expected_fields: list[str] = [
            "oauth2",
            "access_token",
            "token_type",
            "access_token_expiry",
            "refresh_token",
            "refresh_token_expiry",
            "scope",
        ]
        serializer: serializers.FortyTwoTokenSerializer = self.Serializer(
            data=empty_data
        )
        self.assertFalse(serializer.is_valid())
        for key in expected_fields:
            self.assertEqual(serializer.errors[key][0].code, REQUIRED)

    def test_validate_none_data(self) -> None:
        """
        Noneの場合、期待通りにエラーを返すかを確認するテスト
        """
        serializer: serializers.FortyTwoTokenSerializer = self.Serializer(
            data=None
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["non_field_errors"][0].code, "null")

    # todo: invalidなserializerのテストを書く
