from datetime import datetime, timedelta

from django.test import TestCase

from ... import create_oauth2_account, models


class CreateOAuth2AccountTestCase(TestCase):
    """
    OAuth2アカウント関連の機能をテストするクラス。
    """

    def setUp(self) -> None:
        self.user = models.User.objects.create(
            username="pong", email="pong@example.com", password=""
        )
        self.provider_id = "123456"
        self.tokens = {
            "access_token": "dummy_access_token",
            "access_token_expiry": (
                datetime.now() + timedelta(hours=1)
            ).isoformat(),
            "refresh_token": "dummy_refresh_token",
            "refresh_token_expiry": (
                datetime.now() + timedelta(days=30)
            ).isoformat(),
            "scope": "public",
            "token_type": "bearer",
        }

    def test_create_oauth2_user(self) -> None:
        """
        OAuth2ユーザーの作成が成功することを確認するテスト
        """
        oauth2_user_result: create_oauth2_account.CreateOAuth2UserResult = (
            create_oauth2_account.create_oauth2_user("pong@gmail.com", "pong")
        )
        self.assertTrue(oauth2_user_result.is_ok)
