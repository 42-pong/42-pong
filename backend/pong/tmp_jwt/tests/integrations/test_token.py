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
        response_data = response.json()["data"]
        self.assertIn("access", response_data)
        self.assertIn("refresh", response_data)
        self.assertTrue(response_data["access"])
        self.assertTrue(response_data["refresh"])

    def test_api_token_user_not_exists(self) -> None:
        """
        存在しないユーザーのemailでリクエストした場合、'not_exists' エラーが返されることを確認
        """
        data = {
            "email": "nonexistent@example.com",
            "password": self.user.password,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"][0], "not_exists")

    def test_api_token_incorrect_password(self) -> None:
        """
        存在するユーザーのemailで間違ったpasswordを渡した場合、'incorrect_password' エラーが返されることを確認
        """
        data = {"email": self.user.email, "password": "wrongpassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"][0], "incorrect_password")

    def test_api_token_invalid_request(self) -> None:
        """
        emailとpassword以外のリクエストの値を渡した場合、'internal_error' エラーが返されることを確認
        """
        data = {
            "user": 1,
            "email": self.user.email,
            "password": self.user.password,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"][0], "internal_error")
