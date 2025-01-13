from typing import Final

from django.contrib.auth.models import User
from django.test import TestCase

from ... import constants, serializers

ID: Final[str] = constants.UserFields.ID
USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD


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
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertTrue(serializer.is_valid())

    def test_user_serializer_create(self) -> None:
        """
        UserSerializerのcreate()メソッドが正常に動作することを確認する
        """
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )
        if not serializer.is_valid():
            # このテストではerrorにならない想定
            raise AssertionError(serializer.errors)
        user: User = serializer.save()

        self.assertEqual(user.username, self.user_data[USERNAME])
        self.assertEqual(user.email, self.user_data[EMAIL])
        # hash化されていればTrue
        self.assertTrue(user.check_password(self.user_data[PASSWORD]))
        # hash化されているので元のパスワードとは異なる
        self.assertNotEqual(user.password, self.user_data[PASSWORD])

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    def test_user_serializer_none_field_username(self) -> None:
        """
        必須フィールド"username"が存在しない場合にエラーになることを確認する
        """
        self.user_data.pop(USERNAME)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(USERNAME, serializer.errors)

    def test_user_serializer_none_field_email(self) -> None:
        """
        必須フィールド"email"が存在しない場合にエラーになることを確認する
        """
        self.user_data.pop(EMAIL)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)

    def test_user_serializer_none_field_password(self) -> None:
        """
        必須フィールド"password"が存在しない場合にエラーになることを確認する
        """
        self.user_data.pop(PASSWORD)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(PASSWORD, serializer.errors)

    def test_user_serializer_empty_username(self) -> None:
        """
        必須フィールド"username"が空の場合にエラーになることを確認する
        """
        self.user_data[USERNAME] = ""
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(USERNAME, serializer.errors)

    def test_user_serializer_empty_email(self) -> None:
        """
        必須フィールド"email"が空の場合にエラーになることを確認する
        """
        self.user_data[EMAIL] = ""
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)

    def test_user_serializer_empty_password(self) -> None:
        """
        必須フィールド"password"が空の場合にエラーになることを確認する
        """
        self.user_data[PASSWORD] = ""
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(PASSWORD, serializer.errors)

    def test_user_serializer_invalid_email_format(self) -> None:
        """
        emailの形式が不正な場合にエラーになることを確認する
        実装はしていない。models.EmailField()が自動でチェックしてくれている
        """
        self.user_data[EMAIL] = "invalid_email@none"
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)

    def test_user_serializer_duplicate_username(self) -> None:
        """
        既に登録されているusernameが渡された場合にエラーになることを確認する
        実装はしていない。UserModelのUniqueValidatorで自動チェックしてくれている
        """
        # 1人目のUserをDBに保存
        serializer_1: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )
        serializer_1.is_valid(raise_exception=True)
        serializer_1.save()

        # 2人目のUserSerializerを作成
        user_data_2: dict = {
            USERNAME: self.user_data[USERNAME],  # 既に登録されているusername
            EMAIL: "non-exist-email@example.com",
            PASSWORD: "testpassword",
        }
        serializer_2: serializers.UserSerializer = serializers.UserSerializer(
            data=user_data_2
        )

        self.assertFalse(serializer_2.is_valid())
        self.assertIn(USERNAME, serializer_2.errors)

    def test_user_serializer_duplicate_email(self) -> None:
        """
        既に登録されているemailが渡された場合にエラーになることを確認する
        """
        # 1人目のUserをDBに保存
        serializer_1: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )
        serializer_1.is_valid(raise_exception=True)
        serializer_1.save()

        # 2人目のUserSerializerを作成
        user_data_2: dict = {
            USERNAME: "non-exist-user",
            EMAIL: self.user_data[EMAIL],  # 既に登録されているemail
            PASSWORD: "testpassword",
        }
        serializer_2: serializers.UserSerializer = serializers.UserSerializer(
            data=user_data_2
        )

        self.assertFalse(serializer_2.is_valid())
        self.assertIn(EMAIL, serializer_2.errors)
