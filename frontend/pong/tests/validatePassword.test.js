import { describe, expect, it } from "vitest";
import { validatePassword } from "../js/utils/validator/validatePassword";

describe("validatePassword", () => {
  it("should return valid for a correct password format", () => {
    const result = validatePassword("ValidPass123-");
    expect(result).toEqual({
      valid: true,
      message: "パスワードは有効です",
    });
  });

  it("should return invalid for a password that is too short", () => {
    const result = validatePassword("short");
    expect(result).toEqual({
      valid: false,
      message: "パスワードは 8 文字以下禁止です",
    });
  });

  it("should return invalid for a password that is too long", () => {
    const result = validatePassword("a".repeat(51));
    expect(result).toEqual({
      valid: false,
      message: "パスワードは 50 文字以上禁止です",
    });
  });

  it("should return invalid for a password with invalid characters", () => {
    const result = validatePassword("Invalid@Pass");
    expect(result).toEqual({
      valid: false,
      message:
        "パスワードは無効な文字が入っています。（a-zA-Z0-9-_のみ許可）",
    });
  });

  it("should return invalid for a password that is all numbers", () => {
    const result = validatePassword("12345678");
    expect(result).toEqual({
      valid: false,
      message: "パスワードは全て数字が禁止です",
    });
  });

  it("should return valid for a password with valid special characters", () => {
    const result = validatePassword("Valid-Pass_123");
    expect(result).toEqual({
      valid: true,
      message: "パスワードは有効です",
    });
  });
});
