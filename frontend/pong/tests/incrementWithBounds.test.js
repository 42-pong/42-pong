import { describe, expect, it } from "vitest";
import { incrementWithBounds } from "../js/utils/incrementWithBounds";

describe("increments with bouncing back when it hits either lowerBound or upperBound", () => {
  // 簡単な正常テスト
  test(0, 42, 10, 0, 400, 52);
  test(0, 42, -10, 0, 400, 32);
  test(0, 3, -10, 0, 400, 7);
  test(0, 390, 15, 0, 400, 395);

  const shifts = [-42, 0, 42, 1234];
  for (const shift of shifts) {
    // ゼロ移動
    test(shift, 0, 0, 0, 3, 0);
    test(shift, 1, 0, 0, 3, 1);

    // 衝突なし
    test(shift, 0, 1, 0, 3, 1);
    test(shift, 0, 2, 0, 3, 2);
    test(shift, 0, 3, 0, 3, 3);
    test(shift, 1, 1, 0, 3, 2);
    test(shift, 2, 1, 0, 3, 3);
    test(shift, 1, -1, 0, 3, 0);
    test(shift, 2, -1, 0, 3, 1);
    test(shift, 3, -1, 0, 3, 2);
    // upperBound と一回衝突
    test(shift, 0, 4, 0, 3, 2);
    test(shift, 0, 5, 0, 3, 1);
    test(shift, 0, 6, 0, 3, 0);
    // upperBound と一回衝突, その後、lowerBound ともう一回衝突
    test(shift, 0, 7, 0, 3, 1);
    test(shift, 0, 8, 0, 3, 2);
    test(shift, 0, 9, 0, 3, 3);
    // lowerBound と一回衝突
    test(shift, 1, -2, 0, 3, 1);
    test(shift, 1, -3, 0, 3, 2);
  }
});

const withPadding = (num, width = 5) =>
  num.toString().padStart(width);

const test = (
  shift,
  pos,
  delta,
  lowerBound,
  upperBound,
  expectedVal,
) => {
  const shiftedPos = pos + shift;
  const shiftedExpectedVal = expectedVal + shift;
  const shiftedLowerBound = lowerBound + shift;
  const shiftedUpperBound = upperBound + shift;
  it(`${withPadding(shiftedPos)} + ${withPadding(delta)} => ${withPadding(shiftedExpectedVal)}  \trange: [${withPadding(shiftedLowerBound)}, ${withPadding(shiftedUpperBound)}]`, () => {
    expect(
      incrementWithBounds(
        shiftedPos,
        delta,
        shiftedLowerBound,
        shiftedUpperBound,
      ),
    ).toBe(shiftedExpectedVal);
  });
};
