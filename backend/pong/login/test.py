from login import two_factor_auth

# サインアップ時
email = "user@example.com"
issuer_name = "PONG"
qr_code_path = "media/qrs/test.png"

# QRコードを生成し、シークレットキーを取得
secret = two_factor_auth.generate_2fa_qr_code(email, issuer_name, qr_code_path)
print(f"シークレットキー: {secret}")

# ログイン時
user_input = input("Enter the OTP: ")

if two_factor_auth.verify_2fa_totp(secret, user_input):
    print("2FA Verified!")
else:
    print("Invalid OTP")
