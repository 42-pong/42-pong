import { Endpoints } from "../../constants/Endpoints";
import { isNullOrValidId } from "../../utils/isNullOrValidId";
import { fetchAuthenticatedAllData } from "../utils/fetchAuthenticatedAllData";
import { convertTournamentData } from "./convertTournamentData.js";

export async function getTournaments(userId = null) {
  if (!isNullOrValidId(userId))
    return {
      tournaments: [],
      error: new Error("id: not a positive integer"),
    };

  const tournamentsUrl = new URL(Endpoints.TOURNAMENTS.default.href);
  if (userId) tournamentsUrl.searchParams.append("user-id", userId);

  const { data, error } =
    await fetchAuthenticatedAllData(tournamentsUrl);

  const tournaments = error ? [] : data.map(convertTournamentData);
  return { tournaments, error };
}
