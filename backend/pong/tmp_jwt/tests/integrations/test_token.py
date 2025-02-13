from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TokenViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        self.url = reverse("tmp_jwt:token_obtain_pair")

    def test_api_token_success(self) -> None:
        """
        存在するユーザーのemailとpasswordでアクセストークンとリフレッシュトークンが取得できることを確認
        """
        data = {"email": "user@example.com", "password": "password"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # todo: アクセストークンとリフレッシュトークンが返されることを確認
