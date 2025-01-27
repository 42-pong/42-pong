# todo:
# 調査、検討
# - どう関数分けるのがいいのか（simple-jwtのソースコードを読み、参考にする）
# - JWT(RFC7519)の概要を読む
# - DRFを使ってどうユーザーの認証を行うのかについて
# 実装
# - JWTを生成する関数実装
# - payloadを取得する関数実装

from . import base64_url, jws


class JWT:
    """
    JWT (JSON Web Token) に関連する機能を提供するクラス。

    JWTはヘッダー、ペイロード、署名の3部分で構成され、署名はJWSクラスを使用します。

    Attributes:
        payload (dict): JWTのペイロード部分（ユーザー情報など）。

    詳細については、RFC 7519 を参照してください
    https://datatracker.ietf.org/doc/html/rfc7519
    """

    def __init__(self) -> None:
        """
        JWTクラスのインスタンスを初期化。

        Args:
            payload (dict, optional): JWTのペイロード部分。デフォルトはNone。Noneの場合は空の辞書が初期化される。
        """
        # todo: アルゴリズムも選べるようにする？
        self.header: dict = {"typ": "JWT", "alg": "HS256"}
        self.jws: jws.JWS = jws.JWS()
        self.base64_url_handler: base64_url.Base64Url = base64_url.Base64Url()

    def encode(self, payload: dict) -> str:
        """
        引数で渡されたペイロードを検証し、署名済みのJWTを生成します。

        Args:
            todo: ペイロードの詳細な構造を記述
            payload (dict)
                - 必須フィールド: ...
                - 任意フィールド: ...
        Returns:
            str: 署名済みのJWT

        Raises:
            ValueError:
            todo: validate_payload関数作成
            - ペイロードが空である場合
            - ペイロード内の必須フィールドが不足している場合
            - ...

            sign
            - 有効な文字: 英字 (A-Z, a-z), 数字 (0-9), ハイフン (-), アンダースコア (_) 以外の文字が含まれている場合
        """
        # todo: payloadの検証
        encoded_header: str = self.base64_url_handler.encode_dict(self.header)
        encoded_payload: str = self.base64_url_handler.encode_dict(payload)
        encoded_signature: str = self.jws.sign(encoded_header, encoded_payload)
        return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    # @staticmethod
    # def decode(token: str, secret_key: str) -> dict:
    #     """
    #     JWTトークンをデコードする。
    #     """
    #     try:
    #         return jwt.decode(token, secret_key, algorithms=["HS256"])
    #     except jwt.ExpiredSignatureError:
    #         raise ValueError("JWTの有効期限が切れています。")
    #     except jwt.InvalidTokenError:
    #         raise ValueError("無効なJWTトークンです。")
