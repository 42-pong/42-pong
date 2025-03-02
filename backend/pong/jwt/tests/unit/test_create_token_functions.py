from django.test import TestCase

from ...create_token_functions import create_token


class CreateTokenFunctionTestCase(TestCase):
    def setUp(self) -> None:
        self.user_id = 12345

    def test_create_access_token_success(self) -> None:
        token: str = create_token(self.user_id, "access")
        self.assertNotEqual(token, "")

    def test_create_refresh_token_success(self) -> None:
        token: str = create_token(self.user_id, "refresh")
        self.assertNotEqual(token, "")

    def test_invalid_token_type(self) -> None:
        token: str = create_token(self.user_id, "invalid_type")
        self.assertEqual(token, "")
