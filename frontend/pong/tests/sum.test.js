// sum.test.js
import { describe, expect, it } from "vitest";
import { sum } from "../js/sum.js";

describe("let's test sum", () => {
  it("adds 1 + 2 to equal 3", () => {
    expect(sum(1, 2)).toBe(3);
  });
  it("0 + 0 = 0", () => {
    expect(sum(0, 0)).toBe(0);
  });
  it("40 + 2 = 42", () => {
    expect(sum(40, 2)).toBe(42);
  });
  it("4 + 2 != 42", () => {
    expect(sum(4, 2)).not.toBe(42);
  });
});
