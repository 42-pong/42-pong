from datetime import datetime

from django.test import TestCase

from tmp_jwt import jwt_validator


class JsonWebTokenValidatorFunctionTestCase(TestCase):
    def setUp(self) -> None:
        self.jwt_validator: jwt_validator.JWTValidator = (
            jwt_validator.JWTValidator()
        )
        self.now: int = int(datetime.utcnow().timestamp())
        self.payload: dict = {
            "sub": "user123",
            "exp": self.now + 3600,
            "iat": self.now - 3600,
        }

    def test_valid_payload(self) -> None:
        """正常なクレームのみを含むペイロードの場合、検証が通ることを確認するテスト"""
        self.jwt_validator._validate_payload(self.payload)

    def test_invalid_extra_claim(self) -> None:
        """sub, exp, iat以外のクレームを含むペイロードの場合、ValueErrorを投げることを確認するテスト"""
        invalid_payload = self.payload
        invalid_payload["aud"] = "pong"
        with self.assertRaises(ValueError):
            self.jwt_validator._validate_payload(invalid_payload)
