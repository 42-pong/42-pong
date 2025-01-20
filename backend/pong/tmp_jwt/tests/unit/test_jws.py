from django.test import TestCase

from tmp_jwt import jws


class JsonWebSignatureFunctionTestCase(TestCase):
    def setUp(self) -> None:
        self.jws_handler: jws.JWS = jws.JWS()
        self.jws_handler.secret_key = "TEST_SECRET_KEY"
        # {"alg": "HS256", "typ": "JWT"}のBase64エンコード
        self.header_encoded: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        # {"sub": "1234567890"}のBase64エンコード
        self.payload_encoded: str = "eyJzdWIiOiIxMjM0NTY3ODkwIn0"

    def test_sign(self) -> None:
        """
        エンコードされたシグネチャが正しく生成されているかどうかを確認するテスト
        """
        expected_signature: str = "wELfrcYgcf8pyBxSMOCRINRj8QXlxP360D0T3E_bq3U"
        signature_encoded: str = self.jws_handler.sign(
            self.header_encoded, self.payload_encoded
        )
        self.assertEqual(signature_encoded, expected_signature)

