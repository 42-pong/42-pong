import { MessageEnums } from "../../enums/MessageEnums";
import { MessageConstants } from "../../constants/MessageConstants";

const isValidPasswordFormat = (password) => {
  if (password.length < MessageConstants.MIN_LENGTH) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_MIN_LENGTH,
    };
  }

  if (password.length > MessageConstants.MAX_LENGTH) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_MAX_LENGTH,
    };
  }

  if (!MessageConstants.VALID_CHARS.test(password)) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_CHAR,
    };
  }

  if (MessageConstants.ALL_NUMS.test(password)) {
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
