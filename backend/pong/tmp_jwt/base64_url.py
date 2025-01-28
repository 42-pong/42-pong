import base64
import json
import logging
import re

logger = logging.getLogger(__name__)


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
    def decode_bytes(data: str) -> bytes:
        """Base64のurlセーフ形式のデータをデコードする関数"""
        # URLセーフBase64形式の有効性を確認する正規表現
        if not re.match(r"^[A-Za-z0-9\-_]*$", data):
            raise ValueError("Invalid Base64 characters found in input")
        # paddingはエンコードされたデータの長さが 4 の倍数になるように補完するために使用する
        padding: str = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)

    @staticmethod
    def decode_dict(data: str) -> dict:
        """Base64のurlセーフ形式のデータをデコードする関数"""
        data_bytes: bytes = Base64Url.decode_bytes(data)
        try:
            return json.loads(data_bytes)
        except json.JSONDecodeError as e:
            logger.error(f"{data_bytes.decode("utf-8")}")
            raise ValueError("Invalid JSON format") from e
