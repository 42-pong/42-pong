import base64


class Base64Url:
    @staticmethod
    def encode(data: bytes) -> str:
        """データをBase64のurlセーフな形式にエンコードする関数"""
        # bはバイト列を表す
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    @staticmethod
    def decode(data: str) -> bytes:
        """Base64のurlセーフな形式のデータをデコードする関数"""
        # paddingはエンコードされたデータの長さが 4 の倍数になるように補完するために使用する
        padding: str = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)
