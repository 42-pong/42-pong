# todo:
# 調査、検討
# - どう関数分けるのがいいのか（simple-jwtのソースコードを読み、参考にする）
# - JWT(RFC7519)の概要を読む
# - DRFを使ってどうユーザーの認証を行うのかについて
# 実装
# - JWTを生成する関数実装
# - payloadを取得する関数実装

import logging

from . import base64_url, jws

logger = logging.getLogger(__name__)


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
        # todo:　エンコーディング方式をbase64urlに指定する
        self.jws_handler: jws.JWS = jws.JWS()
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
            - ペイロードが空である場合
            - ペイロード内の必須フィールドが不足している場合
            - ...
        """
        # todo: payloadの検証
        encoded_header: str = self.base64_url_handler.encode_dict(self.header)
        encoded_payload: str = self.base64_url_handler.encode_dict(payload)
        encoded_signature: str = self.jws_handler.sign(
            encoded_header, encoded_payload
        )
        return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    def decode(self, jwt: str) -> dict:
        """
        引数で渡されたJWTを検証し、有効期限が保証されたペイロードをデコードして取得します。
        Args:
            jwt (str): 検証対象のJWT。

        Returns:
            dict: 有効期限が保証されたデコード済みのペイロード。

        Raises:
            ValueError:
            - .の数が2個未満のJWTの形式の場合
            - JWTの検証が失敗した場合
            - JWTが有効期限切れの場合。
        """
        try:
            header, payload, signature = jwt.split(".")
        except ValueError:
            logger.error({jwt})
            raise ValueError(
                "Invalid JWT format: must contain exactly two dots"
            )
        if self.jws_handler.verify(header, payload, signature):
            decoded_payload: dict = self.base64_url_handler.decode_dict(
                payload
            )
            # todo: payloadの有効期限が切れていないかどうか
            return decoded_payload
        else:
            logger.error({jwt})
            raise ValueError(
                "JWT Signature verification failed: Invalid or tampered signature"
            )
