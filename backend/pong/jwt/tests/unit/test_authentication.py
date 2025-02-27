from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from ... import authentication, jwt


class CustomJWTAuthenticationTestCase(APITestCase):
    def setUp(self) -> None:
        """テスト用のセットアップ"""
        self.url = "/api/"
        self.factory = APIRequestFactory()
        self.jwt_handler: jwt.JWT = jwt.JWT()
        self.auth_handler: authentication.CustomJWTAuthentication = (
            authentication.CustomJWTAuthentication()
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.now: int = int(datetime.utcnow().timestamp())
        self.payload: dict = {
            "sub": self.user.id,
            "exp": self.now + 3600,
            "iat": self.now - 3600,
            "typ": "access",
        }
        self.valid_token: str = self.jwt_handler.encode(self.payload)
        self.auth_header: dict = {
            "HTTP_AUTHORIZATION": f"Bearer {self.valid_token}"
        }

    def test_authenticate_valid_user(self) -> None:
        """有効なユーザーで Bearer 認証が成功することを確認"""
        request: Request = self.factory.get(self.url, **self.auth_header)
        auth_result = self.auth_handler.authenticate(request)
        self.assertIsNotNone(auth_result)
        if auth_result is None:
            return
        user, token = auth_result
        self.assertEqual(user, self.user)
        self.assertEqual(token, self.valid_token)

    def test_authenticate_no_token(self) -> None:
        """トークン形式の情報が存在しないのリクエストの場合、認証をスキップすることを確認"""
        request: Request = self.factory.get(self.url)
        self.assertIsNone(self.auth_handler.authenticate(request))

    def test_authenticate_invalid_format(self) -> None:
        """Bearer形式でないトークン認証のリクエストの場合、認証をスキップすることを確認"""
        request: Request = self.factory.get(
            self.url, HTTP_AUTHORIZATION="InvalidFormatToken"
        )
        self.assertIsNone(self.auth_handler.authenticate(request))

    def test_authenticate_invalid_token(self) -> None:
        """無効なトークンの場合に AuthenticationFailed が発生し、無効なトークンであること"""
        request: Request = self.factory.get(
            self.url, HTTP_AUTHORIZATION="Bearer invalid_token"
        )
        with self.assertRaises(AuthenticationFailed) as e:
            self.auth_handler.authenticate(request)
        self.assertEqual(e.exception.get_codes(), "invalid_token")

    def test_authenticate_user_not_exist(self) -> None:
        """存在しないユーザーIDを含んだトークンの場合、AuthenticationFailed が発生し、ユーザーが存在しないことを確認"""
        self.payload["sub"] = 99999
        invalid_payload_token: str = self.jwt_handler.encode(self.payload)
        request: Request = self.factory.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {invalid_payload_token}"
        )
        with self.assertRaises(AuthenticationFailed) as e:
            self.auth_handler.authenticate(request)
        self.assertEqual(e.exception.get_codes(), "not_exists")

    def test_authenticate_empty_payload_in_token(self) -> None:
        """ペイロードが空のトークンの場合、AuthenticationFailed が発生し、無効なトークンであることを確認"""
        invalid_payload_token: str = self.jwt_handler.encode({})
        request: Request = self.factory.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {invalid_payload_token}"
        )
        with self.assertRaises(AuthenticationFailed) as e:
            self.auth_handler.authenticate(request)
        self.assertEqual(e.exception.get_codes(), "invalid_token")
