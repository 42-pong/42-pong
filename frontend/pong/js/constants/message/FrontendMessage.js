import { AuthConstants } from "../AuthConstants";

const Auth = {
  LOGIN_ERROR: "メールアドレス、あるいはパスワードが間違えました",
  EMAIL_VALID: "メールアドレスが有効です",
  EMAIL_INVALID_FORMAT: "メールアドレスの形が間違えました",
  PASSWORD_VALID: "パスワードが有効です",
  PASSWORD_INVALID_MIN_LENGTH: `パスワードは ${AuthConstants.MIN_LENGTH} 文字以下禁止です`,
  PASSWORD_INVALID_MAX_LENGTH: `パスワードは ${AuthConstants.MAX_LENGTH} 文字以上禁止です`,
  PASSWORD_INVALID_CHAR: "パスワードは無効な文字が入っています。（大小英数字のみ許可）",
  PASSWORD_INVALID_ALL_NUMS: "パスワードは全て数字が禁止です",
};

export const FrontendMessage = {
  Auth,
}