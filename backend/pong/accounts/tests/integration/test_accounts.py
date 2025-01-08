from typing import Final

from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from ... import constants, models

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD
USER: Final[str] = constants.PlayerFields.USER


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
            "user": {
                USERNAME: "testuser",
                EMAIL: "testuser@example.com",
                PASSWORD: "testpassword12345",
            }
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_user: dict = response.data[USER]

        # responseの内容を確認
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user[USERNAME], "testuser")
        self.assertEqual(response_user[EMAIL], "testuser@example.com")
        # passwordは返されない
        self.assertNotIn(PASSWORD, response_user)

        # DBの状態を確認
        self.assertEqual(models.Player.objects.count(), 1)
        player: models.Player = models.Player.objects.get(
            user__username="testuser"
        )
        self.assertEqual(player.user.email, "testuser@example.com")

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    def test_create_account_with_invalid_data(self) -> None:
        """
        無効なデータでアカウントを作成するテスト
        status 400 が返されることを確認
        ErrorDetail に username, email が含まれることを確認
        """
        account_data: dict = {
            "user": {
                USERNAME: "",  # 空のusername
                EMAIL: "invalid-email@none",  # 不正なemail
                PASSWORD: "testpassword12345",
            }
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_error: dict = response.data["error"]

        # responseの内容を確認
        # response.data = {
        #     "error": {
        #         "username": [
        #             ErrorDetail(string="This field may not be blank.", code="blank")
        #         ],
        #         "email": [
        #             ErrorDetail(string="Enter a valid email address.", code="invalid")
        #         ],
        #     }
        # }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(USERNAME, response_error)
        self.assertIn(EMAIL, response_error)

        # DBの状態を確認
        self.assertEqual(models.Player.objects.count(), 0)
