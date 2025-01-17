import base64


class Base64Url:
    @staticmethod
    def encode(data: bytes) -> str:
        """データをBase64のurlセーフな形式にエンコードする関数"""
        # bはバイト列を表す
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")
