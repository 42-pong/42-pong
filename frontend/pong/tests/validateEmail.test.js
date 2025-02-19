import { describe, expect, it } from "vitest";
import { MessageEnums } from "../js/enums/MessageEnums";
import { validateEmail } from "../js/utils/validator/validateEmail";

describe("validateEmail", () => {
  it("should return valid for a correct email format", () => {
    const result = validateEmail("user@example.com");
    expect(result).toEqual({
      valid: true,
      message: MessageEnums.AuthCode.EMAIL_VALID,
    });
  });

  it("should return invalid for an empty email", () => {
    const result = validateEmail("");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.EMAIL_INVALID_FORMAT,
    });
  });

  it("should return invalid for an email without @", () => {
    const result = validateEmail("userexample.com");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.EMAIL_INVALID_FORMAT,
    });
  });

  it("should return invalid for an email with @ at the start", () => {
    const result = validateEmail("@example.com");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.EMAIL_INVALID_FORMAT,
    });
  });

  it("should return invalid for an email with @ at the end", () => {
    const result = validateEmail("user@");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.EMAIL_INVALID_FORMAT,
    });
  });

  it("should return invalid for an email with @ and no domain", () => {
    const result = validateEmail("user@.com");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.EMAIL_INVALID_FORMAT,
    });
  });

  it("should return invalid for an email with spaces", () => {
    const result = validateEmail("user @example.com");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.EMAIL_INVALID_FORMAT,
    });
  });
});
