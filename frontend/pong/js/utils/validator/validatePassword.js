import { AuthConstants } from "../../constants/AuthConstants";
import { MessageEnums } from "../../enums/MessageEnums";

const isValidPasswordFormat = (password) => {
  if (!password) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_LENGTH,
    };
  }

  if (password.length < AuthConstants.PASSWORD_MIN_LENGTH) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_LENGTH,
    };
  }

  if (password.length > AuthConstants.PASSWORD_MAX_LENGTH) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_LENGTH,
    };
  }

  if (!AuthConstants.PASSWORD_REGEX.test(password)) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_CHAR,
    };
  }

  if (AuthConstants.ALL_NUMS.test(password)) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_ALL_NUMS,
    };
  }

  return {
    valid: true,
    message: MessageEnums.AuthCode.PASSWORD_VALID,
  };
};

const validatePassword = (password) => {
  const result = isValidPasswordFormat(password);
  return result;
};

export { validatePassword };
