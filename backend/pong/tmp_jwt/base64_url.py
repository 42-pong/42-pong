import base64
import json
import re


class Base64Url:
    @staticmethod
    def encode_bytes(data: bytes) -> str:
        """データをBase64のurlセーフな形式にエンコードする関数"""
        # bはバイト列を表す
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    @staticmethod
    def encode_dict(data: dict) -> str:
        """ヘッダーをurlセーフ形式のBase64エンコードする関数"""
        # dictからJSON文字列に変換して、bytesにエンコード
        data_json: str = json.dumps(data)
        data_bytes: bytes = data_json.encode("utf-8")
        return Base64Url.encode_bytes(data_bytes)

    @staticmethod
    def decode(data: str) -> bytes:
        """Base64のurlセーフ形式のデータをデコードする関数"""
        # URLセーフBase64形式の有効性を確認する正規表現
        if not re.match(r"^[A-Za-z0-9\-_]*$", data):
            raise ValueError("Invalid Base64 characters found in input")
        # paddingはエンコードされたデータの長さが 4 の倍数になるように補完するために使用する
        padding: str = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)
