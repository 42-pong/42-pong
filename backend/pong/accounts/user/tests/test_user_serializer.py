from typing import Final

import parameterized  # type: ignore[import-untyped]
from django.contrib.auth.models import User
from django.test import TestCase

from ... import constants
from .. import serializers

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
    def test_valid_data(self) -> None:
        """
        正常なデータが渡された場合にエラーにならないことを確認する
        """
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertTrue(serializer.is_valid())

    def test_create_user(self) -> None:
        """
        UserSerializerのcreate_user()が、正常にUserを作成できることを確認する
        usernameはそのまま、emailはnormalizeされ、passwordはハッシュ化されて保存される
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

    @parameterized.parameterized.expand(
        [
            ("8文字の場合", "-g3wicPg"),
            ("50文字の場合", "z" * 50),
            ("英子文字のみ", "abcdefghijklmnopqrstuvwxyz"),
            ("英大文字のみ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            ("記号(-_)のみ", "-_-_-_-_"),
            ("有名なパスワード以外", "uncommon"),
            ("数字以外が含まれる1", "12x34567"),
        ]
    )
    def test_create_user_with_valid_password(
        self, testcase_name: str, valid_password: str
    ) -> None:
        """
        正常なパスワードでUserを作成できることを確認する
          - 8文字以上・50文字以下
          - 英子文字・英大文字・数字・記号(-_)のみ
          - 有名なパスワード以外
          - 数字以外が含まれる
        """
        user_data: dict = {
            USERNAME: "testuser2",
            EMAIL: "testuser2@example.com",
            PASSWORD: valid_password,
        }
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=user_data
        )

        self.assertTrue(serializer.is_valid())

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    def test_error_none_field_username(self) -> None:
        """
        必須フィールド"username"が存在しない場合にエラーになることを確認する
        """
        self.user_data.pop(USERNAME)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(USERNAME, serializer.errors)

    def test_error_none_field_email(self) -> None:
        """
        必須フィールド"email"が存在しない場合にエラーになることを確認する
        """
        self.user_data.pop(EMAIL)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)

    def test_error_none_field_password(self) -> None:
        """
        必須フィールド"password"が存在しない場合にエラーになることを確認する
        """
        self.user_data.pop(PASSWORD)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(PASSWORD, serializer.errors)

    def test_error_empty_username(self) -> None:
        """
        必須フィールド"username"が空の場合にエラーになることを確認する
        """
        self.user_data[USERNAME] = ""
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(USERNAME, serializer.errors)

    def test_error_empty_email(self) -> None:
        """
        必須フィールド"email"が空の場合にエラーになることを確認する
        """
        self.user_data[EMAIL] = ""
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)

    def test_error_empty_password(self) -> None:
        """
        必須フィールド"password"が空の場合にエラーになることを確認する
        """
        self.user_data[PASSWORD] = ""
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(PASSWORD, serializer.errors)

    @parameterized.parameterized.expand(
        [
            # 空文字列はtest_error_empty_email()で確認済み
            ("user_partがない場合", "@example.com"),
            ("@がない場合", "invalid_email.example.com"),
            ("domain_partがない場合", "invalid_email@"),
            (
                "320文字より長い場合",
                "a" * (320 - len("@example.com") + 1) + "@example.com",
            ),
            ("複数の@が含まれる場合", "invalid_email@example@com"),
            (
                "スペースなどの特殊記号が含まれる場合",
                "invalid< >email@example.com",
            ),
        ]
    )
    def test_error_invalid_email_format(
        self, testcase_name: str, invalid_email: str
    ) -> None:
        """
        emailの形式が不正な場合にエラーになることを確認する
        EmailFieldの中でEmailValidator()が自動でチェックしてくれている
        """
        self.user_data[EMAIL] = invalid_email
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)

    def test_error_duplicate_username(self) -> None:
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

    def test_error_duplicate_email(self) -> None:
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

    @parameterized.parameterized.expand(
        [
            # 空文字列はtest_error_empty_password()で確認済み
            ("7文字以下の場合", "mb7asb2"),
            ("51文字以上の場合", "a" * 51),
            ("数字のみの場合", "97251037"),
            ("よく使われてるパスワードの場合1", "password"),
            ("よく使われてるパスワードの場合2", "pass1234"),
            ("よく使われてるパスワードの場合3", "computer"),
            # ("usernameとの類似度が高い場合", "testuser"), # todo: なぜかエラーにならない
            (
                "使用可能文字列以外が含まれる場合(英数字以外)",
                "あいうえおかきく",
            ),
            (
                "使用可能文字列以外が含まれる場合(記号の-_以外)",
                "invalid@password!",
            ),
        ]
    )
    def test_error_invalid_password(
        self, testcase_name: str, invalid_password: str
    ) -> None:
        """
        パスワードが不正な場合にエラーになることを確認する
        """
        self.user_data[PASSWORD] = invalid_password
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(PASSWORD, serializer.errors)

    def test_error_invalid_email_and_invalid_password(self) -> None:
        """
        emailとpasswordの両方が不正な場合に両方エラーになることを確認する
        """
        self.user_data[EMAIL] = "invalid_email"
        self.user_data[PASSWORD] = "invalid_password!!"
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            data=self.user_data
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(EMAIL, serializer.errors)
        self.assertIn(PASSWORD, serializer.errors)
