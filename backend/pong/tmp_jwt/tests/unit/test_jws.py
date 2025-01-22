from django.test import TestCase

from tmp_jwt import jws


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
        jwt: str = f"{self.encoded_header}.{self.encoded_payload}.wELfrcYgcf8pyBxSMOCRINRj8QXlxP360D0T3E_bq3U"
        is_verify: bool = self.jws_handler.verify(jwt)
        self.assertTrue(is_verify)

    def test_verify_invalid_format(self) -> None:
        """JWTの形式が不正な場合、Falseを返すことを確認するテスト"""
        invalid_jwt: str = "invalid.jwt"
        is_verify: bool = self.jws_handler.verify(invalid_jwt)
        self.assertFalse(is_verify)

    def test_verify_empty_jwt(self) -> None:
        """JWTが空の場合、Falseを返すことを確認するテスト"""
        empty_jwt: str = ""
        is_verify: bool = self.jws_handler.verify(empty_jwt)
        self.assertFalse(is_verify)

    def test_verify_signature_mismatch(self) -> None:
        """JWTの署名が一致しない場合、Falseを返すことを確認するテスト"""
        invalid_signature_jwt: str = (
            f"{self.encoded_header}.{self.encoded_payload}.invalid_signature"
        )
        is_verify: bool = self.jws_handler.verify(invalid_signature_jwt)
        self.assertFalse(is_verify)

    def test_verify_empty_signature(self) -> None:
        """JWTの署名が空の場合、Falseを返すことを確認するテスト"""
        empty_signature_jwt: str = (
            f"{self.encoded_header}.{self.encoded_payload}."
        )
        is_verify: bool = self.jws_handler.verify(empty_signature_jwt)
        self.assertFalse(is_verify)
