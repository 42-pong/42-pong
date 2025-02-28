import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { sampleTournaments } from "../utils/createSamples";
import {
  notAuthenticatedHttpResponse,
  verifyToken,
} from "../utils/mockToken";

export const handlers = [
  http.get(
    Endpoints.TOURNAMENTS.withId(":tournamentId").href,
    async ({ request: { headers }, params: { tournamentId } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      const tournament = sampleTournaments.find(
        ({ id }) => id.toString() === tournamentId,
      );

      const responseBody = tournament
        ? {
            status: "ok",
            data: tournament,
          }
        : {
            status: "error",
          };
      return HttpResponse.json(responseBody);
    },
  ),
];
