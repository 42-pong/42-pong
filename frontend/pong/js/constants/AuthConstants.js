const PASSWORD_MIN_LENGTH = 8;
const PASSWORD_MAX_LENGTH = 50;
const PASSWORD_REGEX = /^[a-zA-Z0-9-_]+$/;
const EMAIL_REGEX =
  /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const EMAIL_PATTERN =
  "[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}$";
const ALL_NUMS = /^\d+$/;

export const AuthConstants = Object.freeze({
  PASSWORD_MIN_LENGTH,
  PASSWORD_MAX_LENGTH,
  PASSWORD_REGEX,
  EMAIL_REGEX,
  EMAIL_PATTERN,
  ALL_NUMS,
});
