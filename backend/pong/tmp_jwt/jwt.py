# todo:
# 調査、検討
# - どう関数分けるのがいいのか（simple-jwtのソースコードを読み、参考にする）
# - JWT(RFC7519)の概要を読む
# - DRFを使ってどうユーザーの認証を行うのかについて
# 実装
# - .envでJWT_SECRET_KEYで秘密鍵を定義
# - JWTを生成する関数実装
# - payloadを取得する関数実装

from typing import Optional

from . import jws


class JWT:
    """
    JWT (JSON Web Token) に関連する機能を提供するクラス。

    JWTはヘッダー、ペイロード、署名の3部分で構成され、署名はJWSクラスを使用します。

    Attributes:
        payload (dict): JWTのペイロード部分（ユーザー情報など）。

    詳細については、RFC 7519 を参照してください
    https://datatracker.ietf.org/doc/html/rfc7519
    """

    def __init__(self, payload: Optional[dict] = None):
        """
        JWTクラスのインスタンスを初期化。

        Args:
            payload (dict, optional): JWTのペイロード部分。デフォルトはNone。Noneの場合は空の辞書が初期化される。
        """
        # todo: アルゴリズムも選べるようにする？
        self.header: dict = {"typ": "JWT", "alg": "HS256"}
        self.payload: dict = payload or {}
        # todo: JWT_SECRET_KEYは.envから読み込むようにする
        self.jws: jws.JWS = jws.JWS()
