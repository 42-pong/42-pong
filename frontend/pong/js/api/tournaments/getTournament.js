import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertTournamentData } from "./convertTournamentData";

export async function getTournament(tournamentId) {
  if (!isValidId(tournamentId)) {
    return {
      tournament: null,
      error: new Error("tournamentId: not a positive integer"),
    };
  }

  const { data, error } = await fetchAuthenticatedData(
    Endpoints.TOURNAMENTS.withId(tournamentId).href,
  );

  const tournament = error ? null : convertTournamentData(data);
  return { tournament, error };
}
