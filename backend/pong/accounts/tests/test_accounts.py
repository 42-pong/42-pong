from typing import Final

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
USER: Final[str] = constants.PlayerFields.USER

DATA: Final[str] = custom_response.DATA
ERRORS: Final[str] = custom_response.ERRORS


# todo: 認証付きのテスト追加？
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
    def test_create_account_with_valid_data(self) -> None:
        """
        有効なデータでアカウントを作成するテスト
        status 201, username, email が返されることを確認
        """
        user_data: dict = {
            EMAIL: "testuser@example.com",
            PASSWORD: "testpassword12345",
        }
        account_data: dict = {USER: user_data}
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
        self.assertEqual(response_user[EMAIL], user_data[EMAIL])
        # passwordは返されない
        self.assertNotIn(PASSWORD, response_user)

        # DBにUser,Playerが1つずつ作成されていることを確認
        self.assertEqual(models.User.objects.count(), 1)
        self.assertEqual(models.Player.objects.count(), 1)

        # emailからplayerを取得できる/例外がraiseされないことを確認
        player: models.Player = models.Player.objects.get(
            user__email=user_data[EMAIL]
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
    def test_create_account_with_invalid_email(
        self, testcase_name: str, invalid_email: str
    ) -> None:
        """
        不正なemailの形式でアカウントを作成するテスト
        status 400 が返されることを確認
        errorsにemailが含まれることを確認
        """
        account_data: dict = {
            USER: {
                EMAIL: invalid_email,  # 不正なemail形式
                PASSWORD: "testpassword12345",
            }
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_error: dict = response.data[ERRORS]

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
        # todo: codeを返すようになったらresponse.data[CODE]も確認

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
    def test_create_account_with_invalid_password(
        self, testcase_name: str, invalid_password: str
    ) -> None:
        """
        不正なpasswordの形式でアカウントを作成するテスト
        status 400 が返されることを確認
        errorsにpasswordが含まれることを確認
        """
        account_data: dict = {
            USER: {
                EMAIL: "valid@example.com",
                PASSWORD: invalid_password,  # 不正なpassword形式
            }
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_error: dict = response.data[ERRORS]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(PASSWORD, response_error)
        # todo: codeを返すようになったらresponse.data[CODE]も確認

        # DBにUser,Playerが作成されていないことを確認
        self.assertEqual(models.User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)
