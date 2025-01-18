from typing import Final

from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from pong.response import response as custom_response

from ... import constants, models

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
        account_data: dict = {
            USER: {
                EMAIL: "testuser@example.com",
                PASSWORD: "testpassword12345",
            }
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
        response_user: dict = response.data[DATA][USER]

        # responseの内容を確認
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user[EMAIL], "testuser@example.com")
        # passwordは返されない
        self.assertNotIn(PASSWORD, response_user)

        # DBにUser,Playerが1つずつ作成されていることを確認
        self.assertEqual(models.User.objects.count(), 1)
        self.assertEqual(models.Player.objects.count(), 1)

        # emailからplayerを取得できる/例外がraiseされないことを確認
        player: models.Player = models.Player.objects.get(
            user__email="testuser@example.com"
        )
        # playerから取得したランダム文字列usernameのUserが実際にDBに存在するか確認
        self.assertTrue(
            models.User.objects.filter(username=player.user.username).exists()
        )

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    def test_create_account_with_invalid_email(self) -> None:
        """
        不正なemailの形式でアカウントを作成するテスト
        status 400 が返されることを確認
        errorsにemailが含まれることを確認
        """
        account_data: dict = {
            USER: {
                EMAIL: "invalid-email@none",  # 不正なemail形式
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

        # DBにUser,Playerが作成されていないことを確認
        self.assertEqual(models.User.objects.count(), 0)
        self.assertEqual(models.Player.objects.count(), 0)
