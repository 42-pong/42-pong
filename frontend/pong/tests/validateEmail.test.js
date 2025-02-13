import { describe, expect, it } from "vitest";
import { validateEmail } from "../js/utils/validator/validateEmail";

describe("validateEmail", () => {
  it("should return valid for a correct email format", () => {
    const result = validateEmail("user@example.com");
    expect(result).toEqual({
      valid: true,
      message: "メールアドレスが有効です",
    });
  });

  it("should return invalid for an empty email", () => {
    const result = validateEmail("");
    expect(result).toEqual({
      valid: false,
      message: "メールアドレスの形が間違えました",
    });
  });

  it("should return invalid for an email without @", () => {
    const result = validateEmail("userexample.com");
    expect(result).toEqual({
      valid: false,
      message: "メールアドレスの形が間違えました",
    });
  });

  it("should return invalid for an email with @ at the start", () => {
    const result = validateEmail("@example.com");
    expect(result).toEqual({
      valid: false,
      message: "メールアドレスの形が間違えました",
    });
  });

  it("should return invalid for an email with @ at the end", () => {
    const result = validateEmail("user@");
    expect(result).toEqual({
      valid: false,
      message: "メールアドレスの形が間違えました",
    });
  });

  it("should return invalid for an email with @ and no domain", () => {
    const result = validateEmail("user@.com");
    expect(result).toEqual({
      valid: false,
      message: "メールアドレスの形が間違えました",
    });
  });

  it("should return invalid for an email with @ and no username", () => {
    const result = validateEmail("@example.com");
    expect(result).toEqual({
      valid: false,
      message: "メールアドレスの形が間違えました",
    });
  });

  it("should return invalid for an email with spaces", () => {
    const result = validateEmail("user @example.com");
    expect(result).toEqual({
      valid: false,
      message: "メールアドレスの形が間違えました",
    });
  });
});
