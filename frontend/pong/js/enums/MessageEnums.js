const AuthCode = {
  LOGIN_ERROR: "LOGIN_ERROR",
  EMAIL_VALID: "EMAIL_VALID",
  EMAIL_INVALID_FORMAT: "EMAIL_INVALID_FORMAT",
  PASSWORD_VALID: "PASSWORD_VALID",
  PASSWORD_INVALID_LENGTH: "PASSWORD_INVALID_LENGTH",
  PASSWORD_INVALID_CHAR: "PASSWORD_INVALID_CHAR",
  PASSWORD_INVALID_ALL_NUMS: "PASSWORD_INVALID_ALL_NUMS",
};

const AccountsCode = {
  already_exists: "ALREADY_EXISTS",
  invalid_email: "INVALID_EMAIL",
  invalid_password: "INVALID_PASSWORD",
};

const TokenCode = {
  not_exists: "NOT_EXISTS",
  incorrect_password: "INCORRECT_PASSWORD",
};

const TokenRefreshCode = {
  invalid: "INVALID",
};

export const MessageEnums = Object.freeze({
  AuthCode,
  AccountsCode,
  TokenCode,
  TokenRefreshCode,
});
