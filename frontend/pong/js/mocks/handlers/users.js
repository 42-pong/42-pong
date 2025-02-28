import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { sampleMyInfo, sampleUsers } from "../utils/createSamples";
import {
  notAuthenticatedHttpResponse,
  verifyToken,
} from "../utils/mockToken";

export const handlers = [
  http.get(
    Endpoints.USERS.default.href,
    async ({ request: { headers } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      return HttpResponse.json({
        status: "ok",
        data: sampleUsers,
      });
    },
  ),
  http.get(
    Endpoints.USERS.me().href,
    async ({ request: { headers } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      const responseBody = {
        status: "ok",
        data: sampleMyInfo,
      };
      return HttpResponse.json(responseBody);
    },
  ),
  http.get(
    Endpoints.USERS.withId(":userId").href,
    async ({ request: { headers }, params: { userId } }) => {
      if (!verifyToken(headers))
        return notAuthenticatedHttpResponse();

      const user = sampleUsers.find(
        ({ id }) => id.toString() === userId,
      );

      const responseBody = user
        ? {
            status: "ok",
            data: user,
          }
        : {
            status: "error",
          };
      return HttpResponse.json(responseBody);
    },
  ),
  http.get(Endpoints.USERS.defaultAvatar.href, async () => {
    const imageBuffer = await fetch("/sample.png").then((res) =>
      res.arrayBuffer(),
    );

    return HttpResponse.arrayBuffer(imageBuffer, {
      headers: {
        "Content-Type": "image/png",
      },
    });
  }),
];
