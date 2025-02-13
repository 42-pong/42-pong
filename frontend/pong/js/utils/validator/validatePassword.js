import {
  Auth,
  minLength,
  maxLength,
  validChars,
  allNums,
} from "../../constants/message/Auth";

const isValidPasswordFormat = (password) => {
  if (password.length < minLength) {
    return {
      valid: false,
      message:
        Auth.validatePasswordMessage[
          `Password must be at least ${minLength} characters long`
        ],
    };
  }

  if (password.length > maxLength) {
    return {
      valid: false,
      message:
        Auth.validatePasswordMessage[
          `Password must be no more than ${maxLength} characters long`
        ],
    };
  }

  if (!validChars.test(password)) {
    return {
      valid: false,
      message:
        Auth.validatePasswordMessage[
          "Password contains invalid characters"
        ],
    };
  }

  if (allNums.test(password)) {
    return {
      valid: false,
      message:
        Auth.validatePasswordMessage[
          "Password cannot be all numbers"
        ],
    };
  }

  return {
    valid: true,
    message: Auth.validatePasswordMessage["Password format is valid"],
  };
};

const validatePassword = (password) => {
  const result = isValidPasswordFormat(password);
  if (!result.valid) {
    return result;
  }
  return {
    valid: true,
    message: Auth.validatePasswordMessage["Password format is valid"],
  };
};

export { validatePassword };
