import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { sampleUsers } from "../utils/createSamples";

export const handlers = [
  http.get(Endpoints.USERS.default.href, async () => {
    return HttpResponse.json({
      status: "ok",
      data: sampleUsers,
    });
  }),
  http.get(Endpoints.USERS.withId(":userId").href, async (req) => {
    const {
      params: { userId },
    } = req;
    const user = sampleUsers.find(({ id }) => id === userId);

    const responseBody = user
      ? {
          status: "ok",
          data: user,
        }
      : {
          status: "error",
        };
    return HttpResponse.json(responseBody);
  }),
];
