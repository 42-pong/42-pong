import pyotp
import qrcode  # type: ignore[import-untyped]


def generate_2fa_qr_code(email: str, issuer_name: str, save_path: str) -> str:
    """
    QRコードを生成し、指定されたパスに保存する関数。

    :param email: ユーザーのメールアドレス
    :param issuer_name: 発行元アプリ名
    :param save_path: QRコード画像の保存パス
    """
    # ユーザーごとの一意のシークレットキーを生成
    totp = pyotp.TOTP(pyotp.random_base32())
    secret = totp.secret

    uri = totp.provisioning_uri(email, issuer_name=issuer_name)
    img = qrcode.make(uri)
    img.save(save_path)

    return secret


def verify_2fa_totp(secret: str, user_input: str) -> bool:
    """
    ユーザー入力のワンタイムパスワードが正しいかどうかを検証する関数。

    :param secret: サインアップ時に生成したシークレットキー
    :param user_input: ユーザーが入力したワンタイムパスワード
    :return: OTPが正しければTrue、間違っていればFalse
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(user_input)
