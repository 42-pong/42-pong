from typing import Final

from django.test import TestCase

from ...constants import UserFields
from ...serializers import UserSerializer

ID: Final[str] = UserFields.ID
USERNAME: Final[str] = UserFields.USERNAME
EMAIL: Final[str] = UserFields.EMAIL
PASSWORD: Final[str] = UserFields.PASSWORD


class UserSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.user_data: dict = {
            ID: 1,
            USERNAME: "testuser",
            EMAIL: "testuser@example.com",
            PASSWORD: "testpassword",
        }

    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    def test_user_serializer_valid_data(self) -> None:
        """
        正常なデータが渡された場合にエラーにならないことを確認する
        """
        serializer: UserSerializer = UserSerializer(data=self.user_data)

        self.assertTrue(serializer.is_valid())

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    def test_user_serializer_empty_username(self) -> None:
        """
        必須フィールド"username"が空の場合にエラーになることを確認する
        """
        self.user_data[USERNAME] = ""
        serializer: UserSerializer = UserSerializer(data=self.user_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(USERNAME, serializer.errors)

    def test_user_serializer_empty_email(self) -> None:
        """
        必須フィールド"email"が空の場合にエラーになることを確認する
        """
        self.user_data[EMAIL] = ""
        serializer: UserSerializer = UserSerializer(data=self.user_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)

    def test_user_serializer_empty_password(self) -> None:
        """
        必須フィールド"password"が空の場合にエラーになることを確認する
        """
        self.user_data[PASSWORD] = ""
        serializer: UserSerializer = UserSerializer(data=self.user_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(PASSWORD, serializer.errors)

    def test_user_serializer_invalid_email_format(self) -> None:
        """
        emailの形式が不正な場合にエラーになることを確認する
        実装はしていない。models.EmailField()が自動でチェックしてくれている
        """
        self.user_data[EMAIL] = "invalid_email@none"
        serializer: UserSerializer = UserSerializer(data=self.user_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)
