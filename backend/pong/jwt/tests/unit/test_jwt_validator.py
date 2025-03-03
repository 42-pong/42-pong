from datetime import datetime

import parameterized  # type: ignore[import-untyped]
from django.test import TestCase

from jwt import jwt_validator


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
            "typ": "access",
        }

    def test_valid_payload(self) -> None:
        """正常なクレームのみを含むペイロードの場合、検証が通ることを確認するテスト"""
        self.jwt_validator.validate_payload(self.payload)

    def test_invalid_extra_claim(self) -> None:
        """sub, exp, iat, typ以外のクレームを含むペイロードの場合、ValueErrorを投げることを確認するテスト"""
        invalid_payload: dict = self.payload.copy()
        invalid_payload["aud"] = "pong"
        with self.assertRaises(ValueError):
            self.jwt_validator.validate_payload(invalid_payload)

    @parameterized.parameterized.expand(
        [
            ("'sub' が不足している場合", {"exp", "iat", "typ"}),
            ("'exp' が不足している場合", {"sub", "iat", "typ"}),
            ("'iat' が不足している場合", {"sub", "exp", "typ"}),
            ("'typ' が不足している場合", {"sub", "exp", "iat"}),
        ]
    )
    def test_invalid_missing_required_claims(
        self, _: str, missing_claims: set[str]
    ) -> None:
        """必須クレームが不足しているペイロードの場合に ValueError を投げることを確認するテスト"""
        invalid_payload: dict = {
            key: value
            for key, value in self.payload.items()
            if key in missing_claims
        }
        with self.assertRaises(ValueError):
            self.jwt_validator.validate_payload(invalid_payload)

    @parameterized.parameterized.expand(
        [
            ("subがstr型でない場合", 123),
        ]
    )
    def test_invalid_sub(self, _: str, invalid_sub: str | int) -> None:
        """'sub'が無効な場合にValueErrorを投げることを確認するテスト"""
        invalid_payload: dict = self.payload.copy()
        invalid_payload["sub"] = invalid_sub
        with self.assertRaises(ValueError):
            self.jwt_validator.validate_payload(invalid_payload)

    @parameterized.parameterized.expand(
        [
            ("'exp'が整数でない場合", "not_integer"),
        ]
    )
    def test_invalid_exp(self, _: str, exp_value: str | int) -> None:
        """'exp'が無効な場合にValueErrorを投げることを確認するテスト"""
        invalid_payload: dict = self.payload.copy()
        invalid_payload["exp"] = exp_value
        with self.assertRaises(ValueError):
            self.jwt_validator.validate_payload(invalid_payload)

    @parameterized.parameterized.expand(
        [
            ("'iat'が整数でない場合", "not_integer"),
            (
                "'iat'が現在時刻より未来の場合",
                int(datetime.utcnow().timestamp()) + 3600,
            ),
        ]
    )
    def test_invalid_iat(self, _: str, iat_value: str | int) -> None:
        """'iat'が無効な場合にValueErrorを投げることを確認するテスト"""
        invalid_payload: dict = self.payload.copy()
        invalid_payload["iat"] = iat_value
        with self.assertRaises(ValueError):
            self.jwt_validator.validate_payload(invalid_payload)

    @parameterized.parameterized.expand(
        [
            ("'typ'が文字列でない場合", 123),
            ("'typ'が'access'または'refresh'以外の場合", "invalid_type"),
        ]
    )
    def test_invalid_typ(self, _: str, typ_value: str | int) -> None:
        """'typ'が無効な場合にValueErrorを投げることを確認するテスト"""
        invalid_payload: dict = self.payload.copy()
        invalid_payload["typ"] = typ_value
        with self.assertRaises(ValueError):
            self.jwt_validator.validate_payload(invalid_payload)
