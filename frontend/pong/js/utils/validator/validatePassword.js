import { MessageEnums } from "../../enums/MessageEnums";
import { AuthConstants } from "../../constants/AuthConstants";

const isValidPasswordFormat = (password) => {
  if (password.length < AuthConstants.MIN_LENGTH) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_MIN_LENGTH,
    };
  }

  if (password.length > AuthConstants.MAX_LENGTH) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_MAX_LENGTH,
    };
  }

  if (!AuthConstants.VALID_CHARS.test(password)) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_CHAR,
    };
  }

  if (AuthConstants.ALL_NUMS.test(password)) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWROD_INVALID_ALL_NUMS,
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
