from django.test import TestCase

from ... import create_oauth2_account


class OAuth2AccountFunctionTestCase(TestCase):
    def test_create_oauth2_user(self) -> None:
        oauth2_user_result: create_oauth2_account.CreateOAuth2UserResult = (
            create_oauth2_account.create_oauth2_user("pong@gmail.com", "pong")
        )
        self.assertTrue(oauth2_user_result.is_ok)
