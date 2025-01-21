# todo:
# 調査、検討
# - JWS(RFC7515)の概要を読む
# - DRFを使ってどうユーザーの認証を行うのかについて
# 実装
# - JWSのペイロード内の`exp`クレームを検証して、有効期限を確認するを実装
#   def validate_jws_expiration(self, payload: dict) -> bool:
import hashlib
import hmac
import re

from pong import settings

from . import base64_url


class JWS:
    """JSON Web Signature (JWS) に関連する機能を提供するクラス

    JWSは、JSONオブジェクトの署名を作成し、署名を安全に伝送するための標準化された方法を提供します。

    詳細については、RFC 7515 を参照してください
    https://datatracker.ietf.org/doc/html/rfc7515
    """

    def __init__(self) -> None:
        self.base64_url_handler: base64_url.Base64Url = base64_url.Base64Url()
        self.secret_key: str = settings.JWS_SECRET_KEY

        if not self.secret_key:
            raise ValueError(
                "JWS_SECRET_KEY is not defined in the environment variables."
            )

    def sign(self, encoded_header: str, encoded_payload: str) -> str:
        """エンコードされたヘッダーとペイロードを基に、エンコードされたシグネチャを生成する"""
        if not encoded_header or not encoded_payload:
            raise ValueError("Both header and payload must be provided.")
        # URLセーフBase64形式の有効性を確認する正規表現
        if not re.match(r"^[A-Za-z0-9\-_]*$", encoded_header) or not re.match(
            r"^[A-Za-z0-9\-_]*$", encoded_payload
        ):
            raise ValueError(
                "Invalid characters found in Base64-encoded input. Ensure only alphanumeric characters, '-' and '_' are used."
            )
        signing_input: str = f"{encoded_header}.{encoded_payload}"
        # ハッシュアルゴリズムを引数で受け取る場合はValueErrorを対応する必要あり
        # https://github.com/python/cpython/blob/main/Lib/hmac.py#L38
        signature: bytes = hmac.new(
            self.secret_key.encode("utf-8"),
            signing_input.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature_encoded: str = self.base64_url_handler.encode(signature)
        return signature_encoded

    def verify(self, jwt: str) -> bool:
        """JWTの署名が正しいか検証する"""
        try:
            encoded_header, encoded_payload, provided_signature = jwt.split(
                "."
            )
        except ValueError:
            raise ValueError(
                "Invalid JWS format. Must be 'header.payload.signature'."
            )
        calculated_signature = self.sign(encoded_header, encoded_payload)
        if calculated_signature != provided_signature:
            raise ValueError("Invalid signature.")
        # todo: ペイロードの検証？
        return True
