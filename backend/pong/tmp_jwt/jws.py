# todo:
# 調査、検討
# - JWS(RFC7515)の概要を読む
# - DRFを使ってどうユーザーの認証を行うのかについて
# 実装
#   def verify_jws(self, jws: str) -> bool:
# - 検証する関数実装
# - JWSのペイロード内の`exp`クレームを検証して、有効期限を確認するを実装
#   def validate_jws_expiration(self, payload: dict) -> bool:
import hashlib
import hmac

from pong import settings

from . import base64_url


class JWS:
    """JSON Web Signature (JWS) に関連する機能を提供するクラス

    JWSは、JSONオブジェクトの署名を作成し、署名を安全に伝送するための標準化された方法を提供します。

    詳細については、RFC 7515 を参照してください
    https://datatracker.ietf.org/doc/html/rfc7515
    """

    def __init__(self) -> None:
        self.base64_url_handler = base64_url.Base64Url()
        self.secret_key = settings.JWS_SECRET_KEY

        if not self.secret_key:
            raise ValueError(
                "JWS_SECRET_KEY is not defined in the environment variables."
            )

    def sign(self, header_encoded: str, payload_encoded: str) -> str:
        """エンコードされたヘッダーとペイロードを基に、エンコードされたシグネチャを生成する"""
        signing_input: str = f"{header_encoded}.{payload_encoded}"
        # ハッシュアルゴリズムを引数で受け取る場合はValueErrorを対応する必要あり
        # https://github.com/python/cpython/blob/main/Lib/hmac.py#L38
        signature: bytes = hmac.new(
            self.secret_key.encode("utf-8"),
            signing_input.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature_encoded = self.base64_url_handler.encode(signature)
        return signature_encoded
