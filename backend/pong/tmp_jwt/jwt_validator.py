class JWTValidator:
    def _validate_payload(self, payload: dict) -> None:
        """
        ペイロードを検証する関数

        "sub" (Subject): JWT が対象を示すクレーム。
        - 検証:
            - str型かどうか
            - 62種からなる英数字かどうか
            - 文字数が7文字かどうか

        "exp" (Expiration Time): JWT の有効期限を示すクレーム。有効期限が過ぎるとそのトークンは無効となる。
        - 検証:
            - int型かどうか
            - 現在の時刻以上であるかどうか

        "iat" (Issued At): JWT が発行された時間を示すクレーム。
        - 検証:
            - int型かどうか
            - 現在時刻以下であるかどうか
        """
