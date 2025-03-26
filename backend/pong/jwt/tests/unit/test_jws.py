from datetime import datetime

import parameterized  # type: ignore[import-untyped]
from django.test import TestCase

from jwt import jws


class JsonWebSignatureFunctionTestCase(TestCase):
    def setUp(self) -> None:
        self.jws_handler: jws.JWS = jws.JWS()
        self.jws_handler.secret_key = "TEST_SECRET_KEY"
        # {"alg": "HS256", "typ": "JWT"}のBase64エンコード
        self.encoded_header: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        # {"sub": "1234567890"}のBase64エンコード
        self.encoded_payload: str = "eyJzdWIiOiIxMjM0NTY3ODkwIn0"

    def test_sign(self) -> None:
        """
        エンコードされたシグネチャが正しく生成されているかどうかを確認するテスト
        """
        expected_signature: str = "wELfrcYgcf8pyBxSMOCRINRj8QXlxP360D0T3E_bq3U"
        encoded_signature: str = self.jws_handler.sign(
            self.encoded_header, self.encoded_payload
        )
        self.assertEqual(encoded_signature, expected_signature)

    def test_sign_empty_header(self) -> None:
        """
        sign関数の引数であるヘッダーが空の場合、ValueErrorが発生することを確認するテスト
        """
        with self.assertRaises(ValueError):
            self.jws_handler.sign("", self.encoded_payload)

    def test_sign_empty_payload(self) -> None:
        """
        sign関数の引数であるペイロードが空の場合、ValueErrorが発生することを確認するテスト。
        """
        with self.assertRaises(ValueError):
            self.jws_handler.sign(self.encoded_header, "")

    def test_sign_empty_header_and_payload(self) -> None:
        """
        sign関数の引数であるヘッダーとペイロードが空の場合、ValueErrorが発生することを確認するテスト。
        """
        with self.assertRaises(ValueError):
            self.jws_handler.sign("", "")

    def test_sign_invalid_base64_header(self) -> None:
        """
        無効なURLセーフBase64エンコード形式のヘッダーが渡された場合に、ValueErrorが発生することを確認するテスト
        """
        invalid_header: str = "#"
        with self.assertRaises(ValueError):
            self.jws_handler.sign(invalid_header, self.encoded_payload)

    def test_sign_invalid_base64_payload(self) -> None:
        """
        無効なURLセーフBase64エンコード形式のペイロードが渡された場合に、ValueErrorが発生することを確認するテスト
        """
        invalid_payload: str = "!"
        with self.assertRaises(ValueError):
            self.jws_handler.sign(self.encoded_header, invalid_payload)

    def test_sign_invalid_base64_header_and_payload(self) -> None:
        """
        無効なURLセーフBase64エンコード形式のヘッダーとペイロードが渡された場合に、ValueErrorが発生することを確認するテスト
        """
        invalid_header: str = "#"
        invalid_payload: str = "!"
        with self.assertRaises(ValueError):
            self.jws_handler.sign(invalid_header, invalid_payload)

    def test_verify(self) -> None:
        """
        JWTの署名が正しい場合、Trueが返されることを確認するテスト
        """
        is_verify: bool = self.jws_handler.verify(
            self.encoded_header,
            self.encoded_payload,
            "wELfrcYgcf8pyBxSMOCRINRj8QXlxP360D0T3E_bq3U",
        )
        self.assertTrue(is_verify)

    @parameterized.parameterized.expand(
        [
            (
                "ヘッダーが空文字の場合",
                "",
                "eyJzdWIiOiIxMjM0NTY3ODkwIn0",
                "wELfrcYgcf8pyBxSMOCRINRj8QXlxP360D0T3E_bq3U",
            ),
            (
                "ペイロードが空文字の場合",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "",
                "wELfrcYgcf8pyBxSMOCRINRj8QXlxP360D0T3E_bq3U",
            ),
            (
                "シグネチャが空文字の場合",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "eyJzdWIiOiIxMjM0NTY3ODkwIn0",
                "",
            ),
            (
                "JWTのシグネチャが一致しない場合",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "eyJzdWIiOiIxMjM0NTY3ODkwIn0",
                "invalid_signature",
            ),
        ]
    )
    def test_verify_invalid(
        self, testcase_name: str, header: str, payload: str, signature: str
    ) -> None:
        is_verify: bool = self.jws_handler.verify(header, payload, signature)
        self.assertFalse(is_verify)

    def test_is_token_expired(self) -> None:
        now: int = int(datetime.utcnow().timestamp())
        payload: dict = {
            "sub": "user123",
            "exp": now + 3600,
            "iat": now - 3600,
            "typ": "access",
        }
        is_token_expired: bool = self.jws_handler.is_token_expired(payload)
        self.assertFalse(is_token_expired)

        payload["exp"] = now - 5000
        is_token_expired = self.jws_handler.is_token_expired(payload)
        self.assertTrue(is_token_expired)
