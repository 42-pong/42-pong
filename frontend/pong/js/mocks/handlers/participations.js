import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { sampleParticipations } from "../utils/createSamples";

export const handlers = [
  http.get(Endpoints.PARTICIPATIONS.href, async ({ request }) => {
    const url = new URL(request.url);
    const tournamentId = Number.parseInt(
      url.searchParams.get("tournament-id"),
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
  }),
];
