from django.contrib.auth.models import User
from django.test import TestCase

from ...constants import UserFields
from ...serializers import UserSerializer

ID: str = UserFields.ID
USERNAME: str = UserFields.USERNAME
EMAIL: str = UserFields.EMAIL
PASSWORD: str = UserFields.PASSWORD


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

    def test_user_serializer_create(self) -> None:
        """
        UserSerializerのcreate()メソッドが正常に動作することを確認する
        """
        serializer: UserSerializer = UserSerializer(data=self.user_data)
        if not serializer.is_valid():
            # このテストではerrorにならない想定
            raise AssertionError(serializer.errors)
        user: User = serializer.save()

        self.assertEqual(user.username, self.user_data[USERNAME])
        self.assertEqual(user.email, self.user_data[EMAIL])

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

    def test_user_serializer_duplicate_username(self) -> None:
        """
        既に登録されているusernameが渡された場合にエラーになることを確認する
        実装はしていない。UserModel関連のどこかで自動チェックしてくれている
        """
        User.objects.create_user(
            username=self.user_data[USERNAME],
            email="non-exist-email@example.com",
            password="testpassword",
        )
        serializer: UserSerializer = UserSerializer(data=self.user_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(USERNAME, serializer.errors)
