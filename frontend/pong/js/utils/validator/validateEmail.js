import { AuthConstants } from "../../constants/AuthConstants";
import { MessageEnums } from "../../enums/MessageEnums";

const isValidEmailFormat = (email) => {
  if (!email) return false; // 入力が空の場合
  if (!AuthConstants.EMAIL_REGEX.test(email)) return false;
  return true;
};

const validateEmail = (email) => {
  if (!isValidEmailFormat(email)) {
    return {
      valid: false,
      message: MessageEnums.AuthCode.EMAIL_INVALID_FORMAT,
    };
  }
  return {
    valid: true,
    message: MessageEnums.AuthCode.EMAIL_VALID,
  };
};

export { validateEmail };
