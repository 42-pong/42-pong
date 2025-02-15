import { MessageEnums } from "../../enums/MessageEnums";

const isValidEmailFormat = (email) => {
  if (!email) return false; // 入力が空の場合
  const atIndex = email.indexOf("@");
  if (atIndex <= 0 || atIndex === email.length - 1) return false; // @マークの前後が空文字列の場合
  if (email[atIndex + 1] === ".") return false; // @マークの後ろが.の場合（ドメインがないケース）
  if (email.includes(" ")) return false; // emailにスペースが入った場合
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
