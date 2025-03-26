import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import {
  getSampleFriends,
  sampleUsers,
} from "../utils/createSamples";
import {
  notAuthenticatedHttpResponse,
  verifyToken,
} from "../utils/mockToken";
import { simpleDeleteResponse } from "../utils/simpleDeleteResponse";
import { simpleErrorResponse } from "../utils/simpleErrorResponse";

export const handlers = [
  http.get(
    Endpoints.FRIENDS.default.href,
    async ({ request: { headers } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      return HttpResponse.json({
        status: "ok",
        data: getSampleFriends(),
      });
    },
  ),
  http.post(Endpoints.FRIENDS.default.href, async ({ request }) => {
    if (!verifyToken(request.headers))
      return notAuthenticatedHttpResponse();

    const { friend_user_id } = await request.json();
    const user = sampleUsers.find(({ id }) => id === friend_user_id);
    if (!(user && !user.is_friend)) return simpleErrorResponse();

    user.is_friend = true;

    return HttpResponse.json({
      status: "ok",
      data: { friend: user },
    });
  }),
  http.delete(
    Endpoints.FRIENDS.withId(":userId").href,
    async ({ request: { headers }, params: { userId } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      const user = sampleUsers.find(
        ({ id }) => id.toString() === userId,
      );
      if (!user?.is_friend) return simpleErrorResponse();

      user.is_friend = false;

      return simpleDeleteResponse();
    },
  ),
];
