from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from ... import constants, models


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
                constants.UserFields.USERNAME: "testuser",
                constants.UserFields.EMAIL: "testuser@example.com",
                constants.UserFields.PASSWORD: "testpassword12345",
            }
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_user: dict = response.data[constants.PlayerFields.USER]

        # responseの内容を確認
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response_user[constants.UserFields.USERNAME], "testuser"
        )
        self.assertEqual(
            response_user[constants.UserFields.EMAIL], "testuser@example.com"
        )
        # passwordは返されない
        self.assertNotIn(constants.UserFields.PASSWORD, response_user)

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
                constants.UserFields.USERNAME: "",  # 空のusername
                constants.UserFields.EMAIL: "invalid-email@none",  # 不正なemail
                constants.UserFields.PASSWORD: "testpassword12345",
            }
        }
        response: drf_response.Response = self.client.post(
            self.url, account_data, format="json"
        )
        response_user: dict = response.data[constants.PlayerFields.USER]

        # responseの内容を確認
        # response.data = {
        #     "user": {
        #         "username": [
        #             ErrorDetail(string="This field may not be blank.", code="blank")
        #         ],
        #         "email": [
        #             ErrorDetail(string="Enter a valid email address.", code="invalid")
        #         ],
        #     }
        # }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(constants.UserFields.USERNAME, response_user)
        self.assertIn(constants.UserFields.EMAIL, response_user)

        # DBの状態を確認
        self.assertEqual(models.Player.objects.count(), 0)
