import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertMatchData } from "./convertMatchData.js";

export async function getMatch(matchId) {
  if (!isValidId(matchId)) {
    return {
      match: null,
      error: new Error("matchId: not a positive integer"),
    };
  }

  const { data, error } = await fetchAuthenticatedData(
    Endpoints.MATCHES.withId(matchId).href,
  );

  const match = error ? null : convertMatchData(data);
  return { match, error };
}
