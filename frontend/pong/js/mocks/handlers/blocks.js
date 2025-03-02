import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { getSampleBlocks, sampleUsers } from "../utils/createSamples";
import {
  notAuthenticatedHttpResponse,
  verifyToken,
} from "../utils/mockToken";
import { simpleDeleteResponse } from "../utils/simpleDeleteResponse";
import { simpleErrorResponse } from "../utils/simpleErrorResponse";

export const handlers = [
  http.get(
    Endpoints.BLOCKS.default.href,
    async ({ request: { headers } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      return HttpResponse.json({
        status: "ok",
        data: getSampleBlocks(),
      });
    },
  ),
  http.post(Endpoints.BLOCKS.default.href, async ({ request }) => {
    if (!verifyToken(request.headers))
      return notAuthenticatedHttpResponse();

    const { blocked_user_id } = await request.json();
    const user = sampleUsers.find(({ id }) => id === blocked_user_id);
    if (!(user && !user.is_blocked)) return simpleErrorResponse();

    user.is_blocked = true;

    return HttpResponse.json({
      status: "ok",
      data: { blocked_user: user },
    });
  }),
  http.delete(
    Endpoints.BLOCKS.withId(":userId").href,
    async ({ request: { headers }, params: { userId } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      const user = sampleUsers.find(
        ({ id }) => id.toString() === userId,
      );
      if (!user?.is_blocked) return simpleErrorResponse();

      user.is_blocked = false;

      return simpleDeleteResponse();
    },
  ),
];
