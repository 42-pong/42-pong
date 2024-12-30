// pos から delta 進んだところを返します。
// lowerBound と upperBound 範囲の外側に進もうとする場合は、その度に逆方向に反転されます。
//
// - 次を前提にしています。
// 1 lowerBound <= upperBound
// 2 lowerBound <= pos <= upperBound
//
// - 簡単な例
// ex) pos = 6 , delta = 5 , range = [0, 10]
//     incrementWithBounds(6,5,0,10) = 9
//
//     - before: [.....x...]
//               01234567890
//
//     - after:  [........x]
//               01234567890
//
export const incrementWithBounds = (
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

  const isOnReflectedRange = basedPos > rangeSize;
  if (isOnReflectedRange)
    basedPos = rangeSize - (basedPos - rangeSize);

  return lowerBound + basedPos;
};
