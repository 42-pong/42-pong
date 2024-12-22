from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from ... import models
from ...constants import UserFields


# todo: 認証付きのテスト追加？
class AccountsTests(APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.url: str = reverse("accounts")

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
                UserFields.USERNAME: "testuser",
                UserFields.EMAIL: "testuser@example.com",
                UserFields.PASSWORD: "testpassword12345",
            }
        }
        response: Response = self.client.post(
            self.url, account_data, format="json"
        )

        # responseの内容を確認
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[UserFields.USERNAME], "testuser")
        self.assertEqual(
            response.data[UserFields.EMAIL], "testuser@example.com"
        )
        # passwordは返されない
        self.assertNotIn(UserFields.PASSWORD, response.data)

        # DBの状態を確認
        self.assertEqual(models.Player.objects.count(), 1)
        player: models.Player = models.Player.objects.get(
            user__username="testuser"
        )
        self.assertEqual(player.user.email, "testuser@example.com")
