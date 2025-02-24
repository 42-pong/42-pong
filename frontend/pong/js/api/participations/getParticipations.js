import { Endpoints } from "../../constants/Endpoints";
import { isNullOrValidId } from "../../utils/isNullOrValidId";
import { fetchData } from "../utils/fetchData";
import { convertParticipationData } from "./convertParticipationData";

export async function getParticipations(
  tournamentId = null,
  userId = null,
) {
  if (!(isNullOrValidId(tournamentId) && isNullOrValidId(userId)))
    return {
      user: null,
      error: new Error("id: not a positive integer"),
    };

  const participationUrl = new URL(Endpoints.PARTICIPATIONS.href);
  if (tournamentId)
    participationUrl.searchParams.append(
      "tournament-id",
      tournamentId,
    );
  if (userId) participationUrl.searchParams.append("user-id", userId);

  const { data, error } = await fetchData(participationUrl);

  const participations = error
    ? []
    : data.map(convertParticipationData);
  return { participations, error };
}
