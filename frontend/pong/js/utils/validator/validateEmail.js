const isValidEmailFormat = (email) => {
  if (!email) {
    return false; // 入力が空の場合
  }

  const atIndex = email.indexOf("@");
  if (atIndex <= 0 || atIndex === email.length - 1) {
    return false; // @マークの前後が空文字列の場合
  }

  return true;
};

const validateEmail = (email) => {
  if (!isValidEmailFormat(email)) {
    return { valid: false, message: "Invalid email format" };
  }

  return { valid: true, message: "Email is valid" };
};

export { validateEmail };
