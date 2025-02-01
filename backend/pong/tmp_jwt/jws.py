# todo:
# 調査、検討
# - JWS(RFC7515)の概要を読む
# - DRFを使ってどうユーザーの認証を行うのかについて
# 実装
# - JWSのペイロード内の`exp`クレームを検証して、有効期限を確認するを実装
#   def validate_jws_expiration(self, payload: dict) -> bool:
import hashlib
import hmac
import logging
from typing import Callable, Dict, TypedDict

from pong import settings

from . import base64_url

logger = logging.getLogger(__name__)


# todo: リファクタリング　エンコーダのタイプ関数を定義するクラス作成
# - encodeとdecodeのタイプを作成する
class EncoderDict(TypedDict):
    encode: Callable[[bytes], str]
    decode: Callable[[str], bytes]


class JWS:
    """JSON Web Signature (JWS) に関連する機能を提供するクラス

    JWSは、JSONオブジェクトの署名を作成し、署名を安全に伝送するための標準化された方法を提供します。

    詳細については、RFC 7515 を参照してください
    https://datatracker.ietf.org/doc/html/rfc7515
    """

    def __init__(self) -> None:
        self.secret_key: str = settings.JWS_SECRET_KEY
        encoding: str = "base64url"
        self.init_encoder_and_decoder(encoding)

    def init_encoder_and_decoder(self, encoding: str) -> None:
        """
        JWSクラスで使用するエンコーディング方式を定義する関数

        Raises:
            ValueError:
            - encodingが対応していないエンコーディング方式名の場合
        """
        base64_url_handler: base64_url.Base64Url = base64_url.Base64Url()
        # todo: JWSの引数にstr型encodingを受け取って、エンコーディングの方式を決める仕様にする
        encoders: Dict[str, EncoderDict] = {
            "base64url": {
                "encode": lambda data: base64_url_handler.encode_bytes(data),
                "decode": lambda data: base64_url_handler.decode_bytes(data),
            }
        }
        if encoding not in encoders:
            raise ValueError(f"Unsupported encoding format: {encoding}")
        self.encoder: Callable[[bytes], str] = encoders[encoding]["encode"]
        self.decoder: Callable[[str], bytes] = encoders[encoding]["decode"]

    def sign(self, encoded_header: str, encoded_payload: str) -> str:
        """エンコードされたヘッダーとペイロードを基に、エンコードされたシグネチャを生成する

        Raises:
            ValueError:
            - encoded_header, encoded_payloadが空文字の場合
            - encoded_header, encoded_payloadが無効なエンコーディング方式の場合
        """
        if not encoded_header or not encoded_payload:
            raise ValueError("Both header and payload must be provided.")
        for name, encoded_data in [
            ("header", encoded_header),
            ("payload", encoded_payload),
        ]:
            try:
                self.decoder(encoded_data)
            except ValueError:
                raise ValueError(
                    f"Invalid characters found in Base64-encoded input {name}."
                )
        signing_input: str = f"{encoded_header}.{encoded_payload}"
        # ハッシュアルゴリズムを引数で受け取る場合はValueErrorを対応する必要あり
        # https://github.com/python/cpython/blob/main/Lib/hmac.py#L38
        signature: bytes = hmac.new(
            self.secret_key.encode("utf-8"),
            signing_input.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature_encoded: str = self.encoder(signature)
        return signature_encoded

    def verify(self, header: str, payload: str, signature: str) -> bool:
        """JWTの署名が正しいか検証する

        Raises:
            ValueError:
            - sign関数の例外
        """
        try:
            calculated_signature: str = self.sign(header, payload)
        except ValueError as e:
            logger.warning(e)
            return False
        # todo: ペイロードの検証？
        if calculated_signature != signature:
            logger.warning("Signature verification failed.")
            return False
        return True
