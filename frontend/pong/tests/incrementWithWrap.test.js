import { describe, expect, it } from "vitest";
import { incrementWithWrap } from "../js/utils/incrementWithWrap";

describe("increments with limiting the result when it hits either lowerBound or upperBound", () => {
  test(1, 0, 0, 10, 1);
  test(1, 1, 0, 10, 2);
  test(1, -1, 0, 10, 0);
  test(0, 10, 0, 10, 10);
  test(0, 11, 0, 10, 10);
  test(0, 20, 0, 10, 10);
  test(10, -10, 0, 10, 0);
  test(10, -20, 0, 10, 0);
  test(10, -42, 0, 10, 0);
  test(42, 10, 0, 400, 52);
  test(42, 1234, 0, 400, 400);
  test(42, -1234, 0, 400, 0);
});

const withPadding = (num, width = 5) =>
  num.toString().padStart(width);

const test = (pos, delta, lowerBound, upperBound, expectedVal) => {
  it(`${withPadding(pos)} + ${withPadding(delta)} => ${withPadding(expectedVal)}  \trange: [${withPadding(lowerBound)}, ${withPadding(upperBound)}]`, () => {
    expect(
      incrementWithWrap(pos, delta, lowerBound, upperBound),
    ).toBe(expectedVal);
  });
};
