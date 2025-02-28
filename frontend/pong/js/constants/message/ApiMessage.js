const Accounts = {
  ALREADY_EXISTS:
    "既にそのメールアドレスでアカウントが作成されています。",
  INVALID_EMAIL: "メールアドレスの形式が間違っています。",
  INVALID_PASSWORD: "パスワードの形式が間違っています。",
};

const Token = {
  NOT_EXISTS: "ユーザーが存在しません。",
  INCORRECT_PASSWORD: "パスワードが間違っています。",
};

const TokenRefresh = {
  INVALID: "再度ログインをしてください。",
};

export const ApiMessage = {
  Accounts,
  Token,
  TokenRefresh,
};
