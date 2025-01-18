// pos から delta 進んだところを返します。
// lowerBound ~ upperBound 範囲の外側に進もうとする場合は、進まずその場所を返します。
//
export const incrementWithWrap = (
  pos,
  delta,
  lowerBound,
  upperBound,
) => {
  let newPos = pos + delta;

  if (newPos < lowerBound) newPos = lowerBound;
  else if (newPos > upperBound) newPos = upperBound;

  return newPos;
};
