import { describe, expect, it } from "vitest";
import { isPreservingDirectionWithBounds } from "../js/utils/isPreservingDirectionWithBounds";

describe("checks whether the proceeding direction is the same, after it proceeds with bouncing back when it hits either lowerBound or upperBound", () => {
  // 簡単な正常テスト
  test(0, 42, 10, 0, 400, true);
  test(0, 42, -10, 0, 400, true);
  test(0, 3, -10, 0, 400, false);
  test(0, 390, 15, 0, 400, false);

  const shifts = [-42, 0, 42, 1234];
  for (const shift of shifts) {
    // ゼロ移動
    test(shift, 0, 0, 0, 3, true);
    test(shift, 1, 0, 0, 3, true);

    // 衝突なし
    test(shift, 0, 1, 0, 3, true);
    test(shift, 0, 2, 0, 3, true);
    test(shift, 0, 3, 0, 3, true);
    test(shift, 1, 1, 0, 3, true);
    test(shift, 2, 1, 0, 3, true);
    test(shift, 1, -1, 0, 3, true);
    test(shift, 2, -1, 0, 3, true);
    test(shift, 3, -1, 0, 3, true);
    // upperBound と一回衝突
    test(shift, 0, 4, 0, 3, false);
    test(shift, 0, 5, 0, 3, false);
    test(shift, 0, 6, 0, 3, false);
    // upperBound と一回衝突, その後、lowerBound ともう一回衝突
    test(shift, 0, 7, 0, 3, true);
    test(shift, 0, 8, 0, 3, true);
    test(shift, 0, 9, 0, 3, true);
    // lowerBound と一回衝突
    test(shift, 1, -2, 0, 3, false);
    test(shift, 1, -3, 0, 3, false);
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
  const shiftedLowerBound = lowerBound + shift;
  const shiftedUpperBound = upperBound + shift;
  it(`${withPadding(shiftedPos)} + ${withPadding(delta)} => ${withPadding(expectedVal)}  \trange: [${withPadding(shiftedLowerBound)}, ${withPadding(shiftedUpperBound)}]`, () => {
    expect(
      isPreservingDirectionWithBounds(
        shiftedPos,
        delta,
        shiftedLowerBound,
        shiftedUpperBound,
      ),
    ).toBe(expectedVal);
  });
};
