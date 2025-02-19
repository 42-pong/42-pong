import { TournamentConstants } from "../../constants/TournamentConstants";

export const isValidTournamentId = (str) => {
  if (!(typeof str === "string")) return false;

  const expectedId = Number.parseInt(str);
  return (
    TournamentConstants.Id.VALID_REGEX().test(str) &&
    !Number.isNaN(expectedId)
  );
};
