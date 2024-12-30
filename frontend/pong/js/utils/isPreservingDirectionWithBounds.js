// pos から delta 進む場合、最終的に最初の進行方向と同じかどうかを返します。
// lowerBound と upperBound 範囲の外側に進もうとする場合は、その度に逆方向に反転されます。
//
// 参考: incrementWithBounds.js
//
export const isPreservingDirectionWithBounds = (
  pos,
  delta,
  lowerBound,
  upperBound,
) => {
  const rangeSize = upperBound - lowerBound;
  const effectiveRangeSize = 2 * rangeSize;

  let basedPos = pos + delta - lowerBound;

  while (basedPos > effectiveRangeSize)
    basedPos -= effectiveRangeSize;

  while (basedPos < 0) basedPos += effectiveRangeSize;

  const isPreservingDirection = basedPos <= rangeSize;
  return isPreservingDirection;
};
