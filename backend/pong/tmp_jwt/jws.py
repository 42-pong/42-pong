# todo:
# 調査、検討
# - JWS(RFC7515)の概要を読む
# - DRFを使ってどうユーザーの認証を行うのかについて
# 実装
# - 署名する関数実装
#   def verify_jws(self, jws: str) -> bool:
# - 検証する関数実装
# - JWSのペイロード内の`exp`クレームを検証して、有効期限を確認するを実装
#   def validate_jws_expiration(self, payload: dict) -> bool:
from pong import settings


class JWS:
    """JSON Web Signature (JWS) に関連する機能を提供するクラス

    JWSは、JSONオブジェクトの署名を作成し、署名を安全に伝送するための標準化された方法を提供します。

    詳細については、RFC 7515 を参照してください
    https://datatracker.ietf.org/doc/html/rfc7515
    """

    def __init__(self) -> None:
        self.secret_key = settings.JWS_SECRET_KEY
        if not self.secret_key:
            raise ValueError(
                "JWS_SECRET_KEY is not defined in the environment variables."
            )
