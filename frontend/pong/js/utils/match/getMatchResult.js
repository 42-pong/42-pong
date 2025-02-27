import { MatchEnums } from "../../enums/MatchEnums";

export const getMatchResult = (player1, player2) => {
  const { PENDING, WIN, LOSE } = MatchEnums.Result;

  if (!(isValid(player1) && isValid(player2)))
    return [PENDING, PENDING];

  const { isWin: isWin1 } = player1;
  const { isWin: isWin2 } = player2;

  if (isWin1 !== isWin2) return isWin1 ? [WIN, LOSE] : [LOSE, WIN];
  return [PENDING, PENDING];
};

const isValid = (player) =>
  player && typeof player.isWin === "boolean";
