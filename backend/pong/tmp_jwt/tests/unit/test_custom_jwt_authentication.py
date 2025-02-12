from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from ... import custom_jwt_authentication, jwt

class CustomJWTAuthenticationTestCase(APITestCase):
    def setUp(self) -> None:
        """テスト用のセットアップ"""
        self.factory = APIRequestFactory()
        self.jwt_handler: jwt.JWT = jwt.JWT()
        self.auth_handler: custom_jwt_authentication.CustomJWTAuthentication = (
            custom_jwt_authentication.CustomJWTAuthentication()
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.now: int = int(datetime.utcnow().timestamp())
        self.payload: dict = {
            "sub": self.user.id,
            "exp": self.now + 3600,
            "iat": self.now - 3600,
            "typ": "access",
        }
        self.valid_token: str = self.jwt_handler.encode(self.payload)
        self.auth_header: dict = {"HTTP_AUTHORIZATION": f"Bearer {self.valid_token}"}

    def test_authenticate_valid_user(self) -> None:
        """有効なユーザーで Bearer 認証が成功することを確認"""
        request: Request = self.factory.get("/api/", **self.auth_header)
        auth_result = self.auth_handler.authenticate(request)
        self.assertIsNotNone(auth_result)
        if auth_result is None:
            return
        user, token = auth_result
        self.assertEqual(user, self.user)
        self.assertEqual(token, self.valid_token)

