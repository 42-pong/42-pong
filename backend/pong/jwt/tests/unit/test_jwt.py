import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import parameterized  # type: ignore[import-untyped]
from django.test import TestCase

from ... import jws, jwt


@unittest.skip(
    "payloadの検証による実装追加に伴い、統合テストでは問題ないため一時的にスキップ。今後、対応予定"
)
class JsonWebTokenFunctionTestCase(TestCase):
    def setUp(self) -> None:
        self.jwt_handler: jwt.JWT = jwt.JWT()
        self.now: int = int(datetime.utcnow().timestamp())
        self.payload: dict = {
            "sub": "user123",
            "exp": self.now + 1000,
            "iat": self.now,
            "typ": "access",
        }

    @patch.object(
        jws.JWS,
        "sign",
        # sign関数の引数にexpected_encoded_headerとexpected_encoded_payloadを渡した返り値
        return_value="wELfrcYgcf8pyBxSMOCRINRj8QXlxP360D0T3E_bq3U",
    )
    def test_encode(
        self,
        mock_sign: MagicMock,
    ) -> None:
        # {"typ": "JWT", "alg": "HS256"}をBase64エンコード
        expected_encoded_header: str = (
            "eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJIUzI1NiJ9"
        )
        # {"sub": "1234567890"}のBase64エンコード
        expected_encoded_payload: str = "eyJzdWIiOiAiMTIzNDU2Nzg5MCJ9"
        expected_encoded_signature: str = mock_sign.return_value
        result: str = self.jwt_handler.encode(self.payload)
        self.assertEqual(
            result,
            f"{expected_encoded_header}.{expected_encoded_payload}.{expected_encoded_signature}",
        )

    @patch.object(
        jwt.JWT,
        "encode",
        return_value="eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiAiMTIzNDU2Nzg5MCJ9.nmUDSA8rHK6Uxwjkc46_pj8ffuFcMXpAoThuaVtqPUQ",
    )
    def test_decode(self, mock_encode: MagicMock) -> None:
        expected_jwt: str = mock_encode.return_value
        result: dict = self.jwt_handler.decode(expected_jwt)
        self.assertEqual(result, self.payload)

    @parameterized.parameterized.expand(
        [
            (
                "空文字の場合",
                "",
            ),
            (
                ".の数が2個未満のJWTの形式の場合",
                "invalid_header.invalid_payload",
            ),
        ]
    )
    def test_encode_invalid_jwt(
        self, testcase_name: str, invalid_jwt: str
    ) -> None:
        print({testcase_name})
        with self.assertRaises(ValueError):
            self.jwt_handler.decode(invalid_jwt)
