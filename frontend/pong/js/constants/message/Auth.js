const minLength = 8;
const maxLength = 50;
const validChars = /^[a-zA-Z0-9-_]+$/;
const allNums = /^\d+$/;

const Auth = {
  validateLoginMessage: "メールアドレス、あるいはパスワードが間違えました",
  validateEmailMessage: {
    "Email is valid": "メールアドレスが有効です",
    "Invalid email format": "メールアドレスの形が間違えました",
  },
  validatePasswordMessage: {
    [`Password must be at least ${minLength} characters long`]: `パスワードは ${minLength} 文字以下禁止です`,
    [`Password must be no more than ${maxLength} characters long`]: `パスワードは ${maxLength} 文字以上禁止です`,
    "Password contains invalid characters":
      "パスワードは無効な文字が入っています。（a-zA-Z0-9-_のみ許可）",
    "Password cannot be all numbers":
      "パスワードは全て数字が禁止です",
    "Password format is valid": "パスワードは有効です",
  },
};

export { Auth, minLength, maxLength, validChars, allNums };
