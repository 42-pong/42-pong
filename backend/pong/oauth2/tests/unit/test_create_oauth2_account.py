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

    def test_create_forty_two_authorization(self) -> None:
        """
        User, OAuth2, FortyTwoTokenが正しく関連付けられ、作成が成功することを確認するテスト
        """
        forty_two_authorization_result: create_oauth2_account.CreateFortyTwoAuthorizationResult = create_oauth2_account.create_forty_two_authorization(
            self.user.id, self.provider_id, self.tokens
        )

        self.assertTrue(forty_two_authorization_result.is_ok)
        oauth2: models.OAuth2 = forty_two_authorization_result.unwrap()

        self.assertEqual(oauth2.user.id, self.user.id)
        self.assertEqual(oauth2.provider, "42")
        self.assertEqual(oauth2.provider_id, self.provider_id)

        # todo: fortytwotokenの全パラメータが存在するかどうか
        forty_two_token: models.FortyTwoToken = (
            models.FortyTwoToken.objects.get(oauth2=oauth2)
        )
        self.assertEqual(forty_two_token.oauth2.id, oauth2.id)
        self.assertEqual(
            forty_two_token.access_token, self.tokens["access_token"]
        )
