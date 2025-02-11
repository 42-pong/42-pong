import { describe, expect, it } from "vitest";
import { validatePassword } from "../js/utils/validator/validatePassword";

describe("validatePassword", () => {
  it("should return valid for a correct password format", () => {
    const result = validatePassword("ValidPass123-");
    expect(result).toEqual({
      valid: true,
      message: "Password is valid",
    });
  });

  it("should return invalid for a password that is too short", () => {
    const result = validatePassword("short");
    expect(result).toEqual({
      valid: false,
      message: "Password must be at least 8 characters long",
    });
  });

  it("should return invalid for a password that is too long", () => {
    const result = validatePassword("a".repeat(51));
    expect(result).toEqual({
      valid: false,
      message: "Password must be no more than 50 characters long",
    });
  });

  it("should return invalid for a password with invalid characters", () => {
    const result = validatePassword("Invalid@Pass");
    expect(result).toEqual({
      valid: false,
      message: "Password contains invalid characters",
    });
  });

  it("should return invalid for a password that is all numbers", () => {
    const result = validatePassword("12345678");
    expect(result).toEqual({
      valid: false,
      message: "Password cannot be all numbers",
    });
  });

  it("should return valid for a password with valid special characters", () => {
    const result = validatePassword("Valid-Pass_123");
    expect(result).toEqual({
      valid: true,
      message: "Password is valid",
    });
  });
});
