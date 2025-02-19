import { describe, expect, it } from "vitest";
import { MessageEnums } from "../js/enums/MessageEnums";
import { validatePassword } from "../js/utils/validator/validatePassword";

describe("validatePassword", () => {
  it("should return valid for a correct password format", () => {
    const result = validatePassword("ValidPass123-");
    expect(result).toEqual({
      valid: true,
      message: MessageEnums.AuthCode.PASSWORD_VALID,
    });
  });

  it("should return valid for a password with valid special characters", () => {
    const result = validatePassword("Valid-Pass_123");
    expect(result).toEqual({
      valid: true,
      message: MessageEnums.AuthCode.PASSWORD_VALID,
    });
  });

  it("should return invalid for a password that is too short", () => {
    const result = validatePassword("short");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_MIN_LENGTH,
    });
  });

  it("should return invalid for a password that is too long", () => {
    const result = validatePassword("a".repeat(51));
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_MAX_LENGTH,
    });
  });

  it("should return invalid for a password with invalid characters", () => {
    const result = validatePassword("Invalid@Pass");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_CHAR,
    });
  });

  it("should return invalid for a password that is all numbers", () => {
    const result = validatePassword("12345678");
    expect(result).toEqual({
      valid: false,
      message: MessageEnums.AuthCode.PASSWORD_INVALID_ALL_NUMS,
    });
  });
});
