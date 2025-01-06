from django.test import TestCase

from oauth2 import models, serializers


class UserSerializerTestCase(TestCase):
    def setUp(self) -> None:
        """
        unittest.TestCaseのsetUpメソッドをオーバーライドして、テスト実行前に必要な初期設定を行う関数

        初期設定
        - self.SerializerにUserSerializerのインスタンスを代入
        """
        self.Serializer: serializers.UserSerializer = (
            serializers.UserSerializer
        )

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

    def test_serializer_with_missing_required_field(self):
        """
        必須フィールドが存在しない場合、期待通りにエラーを返すかを確認するテスト

        必須フィールド
        - username
        - email
        - password
        """
        missing_required_fields_data: dict = {"username": "pong"}
        required_field_error_message: str = "This field is required."
        serializer: serializers.UserSerializer = self.Serializer(
            data=missing_required_fields_data
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.data, {"username": "pong"})
        self.assertEqual(
            serializer.errors["email"][0], required_field_error_message
        )
        self.assertEqual(
            serializer.errors["password"][0], required_field_error_message
        )

    def test_validate_empty_data(self) -> None:
        """
        空のデータの場合、期待通りにエラーを返すかを確認するテスト

        必須フィールド
        - username
        - email
        - password
        """
        empty_data: dict = {}
        required_field_error_message: str = "This field is required."
        serializer: serializers.UserSerializer = self.Serializer(
            data=empty_data
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["username"][0], required_field_error_message
        )
        self.assertEqual(
            serializer.errors["email"][0], required_field_error_message
        )
        self.assertEqual(
            serializer.errors["password"][0], required_field_error_message
        )

    def test_validate_none_data(self) -> None:
        """
        Noneの場合、期待通りにエラーを返すかを確認するテスト
        """
        none_data: dict = None
        none_error_message: str = "No data provided"
        serializer: serializers.UserSerializer = self.Serializer(
            data=none_data
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0], none_error_message
        )

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
        self.assertEqual(serializer.errors["provider_id"][0].code, "unique")

    def test_serializer_with_missing_required_field(self) -> None:
        """
        必須フィールドが存在しない場合、期待通りにエラーを返すかを確認するテスト

        必須フィールド
        - user
        - provider
        - provider_id
        """
        missing_required_fields_data: dict = {"provider": "42"}
        required_field_error_message: str = "This field is required."
        serializer: serializers.OAuth2Serializer = self.Serializer(
            data=missing_required_fields_data
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.errors["user"][0], required_field_error_message)
        self.assertEqual(
            serializer.errors["provider_id"][0], required_field_error_message
        )

    def test_validate_empty_data(self) -> None:
        """
        空のデータの場合、期待通りにエラーを返すかを確認するテスト

        必須フィールド
        - user
        - provider
        - provider_id
        """
        empty_data: dict = {}
        required_field_error_message: str = "This field is required."
        serializer = self.Serializer(data=empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["user"][0], required_field_error_message)
        self.assertEqual(serializer.errors["provider"][0], required_field_error_message)
        self.assertEqual(
            serializer.errors["provider_id"][0], required_field_error_message
        )

    def test_validate_none_data(self) -> None:
        """
        Noneの場合、期待通りにエラーを返すかを確認するテスト
        """
        none_data: dict = None
        none_error_message: str = "No data provided"
        serializer = self.Serializer(data=none_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["non_field_errors"][0], none_error_message)


class FortyTwoTokenSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user: models.User = models.User.objects.create_user(
            username="pong", email="pong@example.com", password=""
        )
        self.oauth2: models.OAuth2 = models.OAuth2.objects.create(
            user=self.user, provider="42", provider_id="12345"
        )
        self.Serializer: serializers.FortyTwoTokenSerializer = (
            serializers.FortyTwoTokenSerializer
        )

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
        self.assertEqual(
            serializer.validated_data["access_token"],
            expected_data["access_token"],
        )
        self.assertEqual(
            serializer.validated_data["token_type"],
            expected_data["token_type"],
        )
        self.assertEqual(
            serializer.validated_data["refresh_token"],
            expected_data["refresh_token"],
        )
        self.assertEqual(
            serializer.validated_data["scope"], expected_data["scope"]
        )

        self.assertEqual(
            serializer.data["token_type"], expected_data["token_type"]
        )
        self.assertEqual(serializer.data["scope"], expected_data["scope"])

        self.assertNotIn("access_token", serializer.data)
        self.assertNotIn("refresh_token", serializer.data)

        self.assertEqual(serializer.errors, {})
