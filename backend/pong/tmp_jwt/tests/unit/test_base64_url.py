import parameterized  # type: ignore[import-untyped]
from django.test import TestCase

from tmp_jwt import base64_url


class Base64UrlTestCase(TestCase):
    def setUp(self) -> None:
        self.base64_url_handler = base64_url.Base64Url()

    def test_encode_bytes(self) -> None:
        """
        bytes型のデータが期待したBase64のURLセーフな形式にエンコードされてるかどうかを確認するテスト。
        """
        data: bytes = b"test_data"
        expected_encoded_data: str = "dGVzdF9kYXRh"
        encoded_data: str = self.base64_url_handler.encode_bytes(data)
        self.assertEqual(encoded_data, expected_encoded_data)

    def test_encode_empty_data(self) -> None:
        """空のデータをエンコードした場合、str型の空文字を返すことを確認するテスト"""
        empty_data: bytes = b""
        expected_encoded_data: str = ""
        encoded_data: str = self.base64_url_handler.encode_bytes(empty_data)
        self.assertEqual(encoded_data, expected_encoded_data)

    @parameterized.parameterized.expand(
        [
            (
                "JWTにあるヘッダーを想定するdict型のデータ",
                {"typ": "JWT", "alg": "HS256"},
                "eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJIUzI1NiJ9",
            ),
            (
                "JWTにあるペイロードーを想定するdict型のデータ",
                {"sub": "1234567890"},
                "eyJzdWIiOiAiMTIzNDU2Nzg5MCJ9",
            ),
            # dump()だとValueErrorの例外を投げるが、dumps()だとobjをJSON形式のstrオブジェクトに直列化するため例外を投げない想定
            # 詳細 https://docs.python.org/ja/3.13/library/json.html#json.dumps
            (
                "dump()だとValueErrorを投げるdict型のデータ",
                {"key": float("nan")},
                "eyJrZXkiOiBOYU59",
            ),
        ]
    )
    def test_encode_dict(
        self, testcase_name: str, data: dict, expected_encoded_data: str
    ) -> None:
        """正常なデータがBase64でdict型のデータにエンコードされるかをテスト

        Args:
            testcase_name: テストケースの説明
            data: dict型のデータ
            expected_encoded_data: 期待するエンコードしたdata
        """
        encoded_data: str = self.base64_url_handler.encode_dict(data)
        self.assertEqual(expected_encoded_data, encoded_data)

    def test_encode_dict_invalid(self) -> None:
        """シリアライズ可能なJSON形式ではないdict型のデータの場合、TypeErrorかどうかを確認するテスト"""
        data: dict = {"key": {1, 2, 3}}
        with self.assertRaises(TypeError):
            self.base64_url_handler.encode_dict(data)

    def test_decode_bytes(self) -> None:
        """
        utf-8の文字フォーマットの=なしのエンコードのデータからbytes型のデータに変換しているかどうか確認するテスト
        """
        encoded_data: str = "dGVzdF9kYXRh"
        expected_decoded_data: bytes = b"test_data"
        decoded_data: bytes = self.base64_url_handler.decode_bytes(
            encoded_data
        )
        self.assertEqual(decoded_data, expected_decoded_data)

    def test_decode_empty_data(self) -> None:
        """空のデータをデコードした場合、バイト型の空文字を返すことを確認するテスト"""
        empty_data: str = ""
        expected_decoded_empty_data: bytes = b""
        decoded_data: bytes = self.base64_url_handler.decode_bytes(empty_data)
        self.assertEqual(decoded_data, expected_decoded_empty_data)

    def test_decode_non_ascii_data(self) -> None:
        """非ASCII文字を含むデータをデコードした場合、ValueErrorを投げることを確認するテスト"""
        non_ascii_data: str = "日本語テキスト"
        with self.assertRaises(ValueError):
            self.base64_url_handler.decode_bytes(non_ascii_data)

    def test_decode_invalid_urlsafe_base64_characters(self) -> None:
        """不正なBase64URLセーフ形式の文字が含まれる場合、ValueErrorを投げることを確認するテスト"""
        invalid_urlsafe_base64_data: str = "invalid!@#$"
        with self.assertRaises(ValueError):
            self.base64_url_handler.decode_bytes(invalid_urlsafe_base64_data)

    def test_encode_decode_bytes_round_trip(self) -> None:
        """Base64URLセーフ形式にbytes型のデータにエンコードし、そのデータをデコードして元のデータに戻ることを確認するテスト"""
        data: bytes = b"test_round_trip"
        encoded_data: str = self.base64_url_handler.encode_bytes(data)
        decoded_data: bytes = self.base64_url_handler.decode_bytes(
            encoded_data
        )
        self.assertEqual(decoded_data, data)

    def test_encode_decode_dict_round_trip(self) -> None:
        """Base64URLセーフ形式にdict型のデータにエンコードし、そのデータをデコードして元のデータに戻ることを確認するテスト"""
        data: dict = {"Key": "Value"}
        encoded_data: str = self.base64_url_handler.encode_dict(data)
        decoded_data: dict = self.base64_url_handler.decode_dict(encoded_data)
        self.assertEqual(decoded_data, data)

    def test_decode_dict_invalid_json(self) -> None:
        """
        Base64URLセーフ形式のデータをdict型のデータにデコードした後に、そのデータが無効なJSON形式の場合、ValueErrorかどうか確認するテスト。
        """
        encoded_invalid_json_data: str = "aW52YWxpZF9qc29u"
        with self.assertRaises(ValueError):
            self.base64_url_handler.decode_dict(encoded_invalid_json_data)
