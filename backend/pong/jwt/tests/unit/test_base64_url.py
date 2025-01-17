import base64

from django.test import TestCase

from jwt import base64_url


class Base64Url(TestCase):
    def setUp(self) -> None:
        self.base64_url_handler = base64_url.Base64Url()

    def test_encode(self) -> None:
        """
        データをBase64エンコードし、URLセーフな形式に変換後、末尾の'='パディングを取り除いたUTF-8文字列に変換されていることを確認するテスト。
        """
        data = b"test_data"
        expected_encoded_data = (
            base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")
        )
        encoded_data = self.base64_url_handler.encode(data)
        self.assertEqual(encoded_data, expected_encoded_data)

    def test_decode(self) -> None:
        """
        utf-8の文字フォーマットの=なしのエンコードのデータから期待してるデータに変換しているかどうか確認するテスト
        """
        encoded_data = "dGVzdF9kYXRh"
        expected_decoded_data = b"test_data"
        decoded_data = self.base64_url_handler.decode(encoded_data)
        self.assertEqual(decoded_data, expected_decoded_data)
