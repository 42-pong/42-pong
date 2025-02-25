import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { sampleParticipations } from "../utils/createSamples";
import {
  notAuthenticatedHttpResponse,
  verifyToken,
} from "../utils/mockToken";

export const handlers = [
  http.get(
    Endpoints.PARTICIPATIONS.href,
    async ({ request: { url, headers } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      const requestUrl = new URL(url);
      const tournamentId = Number.parseInt(
        requestUrl.searchParams.get("tournament-id"),
      );

      let participations = sampleParticipations;
      if (tournamentId)
        participations = participations.filter(
          (participation) =>
            participation.tournament_id === tournamentId,
        );

      return HttpResponse.json({
        status: "ok",
        data: participations,
      });
    },
  ),
];
