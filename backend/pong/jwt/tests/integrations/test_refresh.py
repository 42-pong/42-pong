from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ... import jwt
from ...create_token_functions import create_token


class RefreshTokenViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="user123", email="user@example.com", password="password"
        )
        self.refresh_token: str = create_token(self.user.username, "refresh")
        self.url = reverse("jwt:token_refresh")
        self.jwt_handler: jwt.JWT = jwt.JWT()

    def test_api_refresh_token_success(self) -> None:
        """
        /api/token/refreshを成功する場合、リフレッシュトークンと同じユーザーIDのアクセストークンを取得できることを確認
        """
        data = {"refresh": self.refresh_token}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]
        self.assertIn("access", response_data)
        response_access_token: str = response_data["access"]
        payload: dict = self.jwt_handler.decode(response_access_token)
        self.assertEqual(payload["sub"], self.user.username)

    def test_api_refresh_token_user_not_exists(self) -> None:
        """
        存在しないユーザのリフレッシュトークンを渡した場合、401のステータスコードと'not_exists' のエラーコードが返されることを確認
        """
        not_exists_refresh_token: str = create_token("123user", "refresh")
        data = {"refresh": not_exists_refresh_token}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"][0], "not_exists")

    def test_api_refresh_token_invalid_refresh_token(self) -> None:
        """
        不正なリフレッシュトークンを渡した場合、401のステータスコードと'invalid' のエラーコードが返されることを確認
        """
        data = {"refresh": "invalid_token"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"][0], "invalid")

    def test_api_refresh_token_access_token_type(self) -> None:
        """
        アクセストークンを渡した場合、401のステータスコードと'invalid' のエラーコードが返されることを確認
        """
        access_token: str = create_token(self.user.username, "access")
        data = {"refresh": access_token}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"][0], "invalid")
