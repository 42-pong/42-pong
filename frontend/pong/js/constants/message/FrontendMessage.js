import { AuthConstants } from "../AuthConstants";

const Auth = {
  LOGIN_ERROR: "メールアドレス、あるいはパスワードが間違えました。",
  EMAIL_VALID: "メールアドレスが有効です。",
  EMAIL_INVALID_FORMAT: "メールアドレスの形が間違えました。",
  PASSWORD_VALID: "パスワードが有効です。",
  PASSWORD_INVALID_LENGTH: `パスワードは ${AuthConstants.PASSWORD_MIN_LENGTH} 文字以上、${AuthConstants.PASSWORD_MAX_LENGTH}文字以下で入力してください。`,
  PASSWORD_INVALID_CHAR:
    "パスワードは無効な文字が入っています。英小文字・英大文字・数字・記号 (-, _)が使用可能です。",
  PASSWORD_INVALID_ALL_NUMS: "数字のみのパスワードは設定できません。",
};

export const FrontendMessage = {
  Auth,
};
