from datetime import datetime, timedelta
from unittest import mock

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

    @mock.patch(
        "accounts.player.identicon.generate_identicon",
        return_value="avatars/sample.png",
    )
    def test_create_oauth2_user(self, mock_identicon: mock.MagicMock) -> None:
        """
        OAuth2ユーザーの作成が成功することを確認するテスト
        """
        oauth2_user_result: create_oauth2_account.CreateOAuth2UserResult = (
            create_oauth2_account.create_oauth2_user("pong@gmail.com", "pong")
        )
        self.assertTrue(oauth2_user_result.is_ok)

    def test_create_oauth2_user_failure_invalid_email(self) -> None:
        """
        不正なemailの形式の場合、OAuth2ユーザーの作成が失敗し、invalidを返すかどうかを確認するテスト
        """
        # todo: django の email バリデーションを調べてからそれをそのまま使うか、自分達で定義するか決める
        oauth2_user_result: create_oauth2_account.CreateOAuth2UserResult = (
            create_oauth2_account.create_oauth2_user(
                "invalid--@gmail-com", "pong"
            )
        )
        self.assertTrue(oauth2_user_result.is_error)
        self.assertEqual(
            oauth2_user_result.unwrap_error()["email"][0].code, "invalid"
        )

    def test_create_oauth2_account(self) -> None:
        """
        OAuth2アカウントの作成が成功し、Userと関連付けられたOAuth2データが保存されることを確認するテスト。
        """
        oauth2_result = create_oauth2_account.create_oauth2(
            self.user.id, "42", self.provider_id
        )
        self.assertTrue(oauth2_result.is_ok)
        oauth2: dict = oauth2_result.unwrap()
        self.assertEqual(oauth2["user"], self.user.id)
        self.assertEqual(oauth2["provider"], "42")
        self.assertEqual(oauth2["provider_id"], self.provider_id)

    def test_create_oauth2_account_failure_user_not_found(self) -> None:
        """
        存在しないユーザーIDを指定した場合にOAuth2アカウント作成が失敗し、does_not_existを返すか確認するテスト。
        """
        invalid_user_id = 99999
        oauth2_result = create_oauth2_account.create_oauth2(
            invalid_user_id, "42", self.provider_id
        )
        self.assertTrue(oauth2_result.is_error)
        self.assertTrue(
            oauth2_result.unwrap_error()["user"][0].code, "does_not_exist"
        )

    # todo: OAuth2Serializerのvalidate関数で42以外のプロバイダーを弾く関数を作成する
    # def test_create_oauth2_account_failure_invalid_provider(self) -> None:
    #     """
    #     42以外のプロバイダー情報でOAuth2アカウント作成が失敗することを確認するテスト。
    #     """
    #     oauth2_result = create_oauth2_account.create_oauth2(
    #         self.user.id, "", self.provider_id
    #     )
    #     self.assertFalse(oauth2_result.is_ok)
    #     self.assertIn("provider", oauth2_result.unwrap_error())
