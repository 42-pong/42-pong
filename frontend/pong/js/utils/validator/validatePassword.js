const isValidPasswordFormat = (password) => {
  const minLength = 8;
  const maxLength = 50;
  const validChars = /^[a-zA-Z0-9-_]+$/;

  if (password.length < minLength) {
    return {
      valid: false,
      message: `Password must be at least ${minLength} characters long`,
    };
  }

  if (password.length > maxLength) {
    return {
      valid: false,
      message: `Password must be no more than ${maxLength} characters long`,
    };
  }

  if (!validChars.test(password)) {
    return {
      valid: false,
      message: "Password contains invalid characters",
    };
  }

  if (/^\d+$/.test(password)) {
    return {
      valid: false,
      message: "Password cannot be all numbers",
    };
  }

  return { valid: true, message: "Password format is valid" };
};

const validatePassword = (password) => {
  const result = isValidPasswordFormat(password);
  if (!result.valid) {
    return result;
  }
  return { valid: true, message: "Password is valid" };
};

export { validatePassword };
