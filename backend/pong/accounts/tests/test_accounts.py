from typing import Final
from unittest import mock

import parameterized  # type: ignore[import-untyped]
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from pong.custom_response import custom_response

from .. import constants
from ..player import models

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD

DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE
ERRORS: Final[str] = custom_response.ERRORS

CODE_ALREADY_EXISTS: Final[str] = constants.Code.ALREADY_EXISTS
CODE_INVALID_EMAIL: Final[str] = constants.Code.INVALID_EMAIL
CODE_INVALID_PASSWORD: Final[str] = constants.Code.INVALID_PASSWORD

MOCK_AVATAR_NAME: Final[str] = "avatars/test.png"


class AccountsTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.url: str = reverse("accounts:account_create")

    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    @mock.patch(
        "accounts.player.identicon.generate_identicon",
        return_value=MOCK_AVATAR_NAME,
    )
    def test_200_create_account_with_valid_data(
        self, mock_identicon: mock.MagicMock
    ) -> None:
        """
        有効なデータでアカウントを作成するテスト
        status 201, username, email が返されることを確認
        """
        account_data: dict = {
            EMAIL: "testuser@example.com",
            PASSWORD: "testpassword12345",
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        # response.data == {
        #     "status": "ok",
        #     "data": {
        #         "user": {...}
        #     },
        # }
        response_user: dict = response.data[DATA]

        # responseの内容を確認
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user[EMAIL], account_data[EMAIL])
        # passwordは返されない
        self.assertNotIn(PASSWORD, response_user)

        # DBにUser,Playerが1つずつ作成されていることを確認
        self.assertEqual(models.User.objects.count(), 1)
        self.assertEqual(models.Player.objects.count(), 1)

        # emailからplayerを取得できる/例外がraiseされないことを確認
        player: models.Player = models.Player.objects.get(
            user__email=account_data[EMAIL]
        )
        # playerから取得したランダム文字列usernameのUserが実際にDBに存在するか確認
        self.assertTrue(
            models.User.objects.filter(username=player.user.username).exists()
        )

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    @parameterized.parameterized.expand(
        [
            ("空文字列の場合", ""),
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
    def test_400_create_account_with_invalid_email(
        self, testcase_name: str, invalid_email: str
    ) -> None:
        """
        不正なemailの形式でアカウントを作成するテスト
        status 400 が返されることを確認
        errorsにemailが含まれることを確認
        """
        account_data: dict = {
            EMAIL: invalid_email,  # 不正なemail形式
            PASSWORD: "testpassword12345",
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_error: dict = response.data[ERRORS]
        code: list[str] = response.data[CODE]

        # responseの内容を確認
        # response.data == {
        #     "status": "error",
        #     "errors": {
        #         "email": [
        #             ErrorDetail(string="Enter a valid email address.", code="invalid")
        #         ],
        #     }
        # }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(EMAIL, response_error)
        self.assertIn(CODE_INVALID_EMAIL, code)

        # DBにUser,Playerが作成されていないことを確認
        self.assertEqual(models.User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)

    @parameterized.parameterized.expand(
        [
            ("空文字列の場合", ""),
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
    def test_400_create_account_with_invalid_password(
        self, testcase_name: str, invalid_password: str
    ) -> None:
        """
        不正なpasswordの形式でアカウントを作成するテスト
        status 400 が返されることを確認
        errorsにpasswordが含まれることを確認
        """
        account_data: dict = {
            EMAIL: "valid@example.com",
            PASSWORD: invalid_password,  # 不正なpassword形式
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_error: dict = response.data[ERRORS]
        code: list[str] = response.data[CODE]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(PASSWORD, response_error)
        self.assertIn(CODE_INVALID_PASSWORD, code)

        # DBにUser,Playerが作成されていないことを確認
        self.assertEqual(models.User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)

    def test_400_invalid_email_and_invalid_password(self) -> None:
        """
        不正なemailと不正なpasswordの形式でアカウントを作成するテスト
        status 400 が返されることを確認
        errorsにemailとpasswordが含まれることを確認
        """
        account_data: dict = {
            EMAIL: "invalid_email",
            PASSWORD: "invalid_password!!",
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_error: dict = response.data[ERRORS]
        code: list[str] = response.data[CODE]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(EMAIL, response_error)
        self.assertIn(PASSWORD, response_error)
        self.assertIn(CODE_INVALID_EMAIL, code)
        self.assertIn(CODE_INVALID_PASSWORD, code)

    @mock.patch(
        "accounts.player.identicon.generate_identicon",
        return_value=MOCK_AVATAR_NAME,
    )
    def test_400_already_exists_email(
        self, mock_identicon: mock.MagicMock
    ) -> None:
        """
        既に存在するemailで再度アカウントを作成しようとするテスト
        status 400 が返されることを確認
        errorsにemailが含まれることを確認
        """
        account_data: dict = {
            EMAIL: "testuser@example.com",
            PASSWORD: "testpassword12345",
        }
        # 1回目のアカウント作成
        response1: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        # 2回目のアカウント作成
        response2: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_error: dict = response2.data[ERRORS]
        code: list[str] = response2.data[CODE]

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(EMAIL, response_error)
        self.assertIn(CODE_ALREADY_EXISTS, code)
