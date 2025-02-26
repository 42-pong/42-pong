import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { sampleFriends } from "../utils/createSamples";
import {
  notAuthenticatedHttpResponse,
  verifyToken,
} from "../utils/mockToken";

export const handlers = [
  http.get(
    Endpoints.FRIENDS.href,
    async ({ request: { headers } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      return HttpResponse.json({
        status: "ok",
        data: sampleFriends,
      });
    },
  ),
];
