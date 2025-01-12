from datetime import datetime, timedelta

from django.test import TestCase

from ... import models, providers


# todo: 各プロバイダのテストケースが多くなったら、それぞれのテストクラスを作成する
class CreateProviderAuthorizationTestCase(TestCase):
    """
    OAuth2の各プロバイダー認証機能をテストするためのクラス
    """

    def setUp(self) -> None:
        self.user = models.User.objects.create(
            username="pong", email="pong@example.com", password=""
        )
        # UserとOAuth2関連してるかどうかのテストで作成するため、OAuth2のモデルは作成しない
        self.provider = "42"
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

    def test_create_forty_two_authorization(self) -> None:
        """
        User, OAuth2, FortyTwoTokenが正しく関連付けられ、作成が成功することを確認するテスト
        """
        forty_two_authorization_result: providers.forty_two_authorization.CreateFortyTwoAuthorizationResult = providers.forty_two_authorization.create_forty_two_authorization(
            self.user.id, self.provider, self.provider_id, self.tokens
        )

        self.assertTrue(forty_two_authorization_result.is_ok)
        oauth2: models.OAuth2 = forty_two_authorization_result.unwrap()

        self.assertEqual(oauth2.user.id, self.user.id)
        self.assertEqual(oauth2.provider, self.provider)
        self.assertEqual(oauth2.provider_id, self.provider_id)

        # todo: fortytwotokenの全パラメータが存在するかどうか
        forty_two_token: models.FortyTwoToken = (
            models.FortyTwoToken.objects.get(oauth2=oauth2)
        )
        self.assertEqual(forty_two_token.oauth2.id, oauth2.id)
        self.assertEqual(
            forty_two_token.access_token, self.tokens["access_token"]
        )

    # todo: 以下のテストケースは後で実装する
    #   - トークンのバリデーション失敗時のケース
    #   - OAuth2作成失敗時のケース
