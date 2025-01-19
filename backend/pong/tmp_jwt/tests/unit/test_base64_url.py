import base64

from django.test import TestCase

from tmp_jwt import base64_url


class Base64UrlTestCase(TestCase):
    def setUp(self) -> None:
        self.base64_url_handler = base64_url.Base64Url()

    def test_encode(self) -> None:
        """
        データをBase64エンコードし、URLセーフな形式に変換後、末尾の'='パディングを取り除いたUTF-8文字列に変換されていることを確認するテスト。
        """
        data: bytes = b"test_data"
        expected_encoded_data = (
            base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")
        )
        encoded_data: str = self.base64_url_handler.encode(data)
        self.assertEqual(encoded_data, expected_encoded_data)

    def test_encode_empty_data(self) -> None:
        """空のデータをエンコードした場合、str型の空文字を返すことを確認するテスト"""
        empty_data: bytes = b""
        expected_encoded_data: str = ""
        encode_data: str = self.base64_url_handler.encode(empty_data)
        self.assertEqual(encode_data, expected_encoded_data)

    def test_decode(self) -> None:
        """
        utf-8の文字フォーマットの=なしのエンコードのデータから期待してるデータに変換しているかどうか確認するテスト
        """
        encoded_data: str = "dGVzdF9kYXRh"
        expected_decoded_data: bytes = b"test_data"
        decoded_data: bytes = self.base64_url_handler.decode(encoded_data)
        self.assertEqual(decoded_data, expected_decoded_data)

    def test_decode_empty_data(self) -> None:
        """空のデータをデコードした場合、バイト型の空文字を返すことを確認するテスト"""
        empty_data: str = ""
        expected_decoded_data: bytes = b""
        decoded_data: bytes = self.base64_url_handler.decode(empty_data)
        self.assertEqual(decoded_data, expected_decoded_data)

    def test_decode_non_ascii_data(self) -> None:
        """非ASCII文字を含むデータをデコードした場合、ValueErrorを投げることを確認するテスト"""
        non_ascii_data: str = "日本語テキスト"
        with self.assertRaises(ValueError):
            self.base64_url_handler.decode(non_ascii_data)

    def test_decode_invalid_urlsafe_base64_characters(self) -> None:
        """URLセーフ形式のBase64に不正な文字が含まれる場合、ValueErrorを投げることを確認するテスト"""
        invalid_urlsafe_base64_data: str = "invalid!@#$"
        with self.assertRaises(ValueError):
            self.base64_url_handler.decode(invalid_urlsafe_base64_data)

    def test_encode_decode_round_trip(self) -> None:
        """Base64エンコードしたデータをデコードして元のデータに戻ることを確認するテスト"""
        data: bytes = b"test_round_trip"
        encoded_data: str = self.base64_url_handler.encode(data)
        decoded_data: bytes = self.base64_url_handler.decode(encoded_data)
        self.assertEqual(decoded_data, data)
