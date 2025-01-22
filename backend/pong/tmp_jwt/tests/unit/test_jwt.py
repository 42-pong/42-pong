from django.test import TestCase

from tmp_jwt import jwt


class JsonWebTokenFunctionTestCase(TestCase):
    def setUp(self) -> None:
        self.jwt_handler: jwt.JWT = jwt.JWT()
