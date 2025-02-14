import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { sampleFriends } from "../utils/createSamples";

export const handlers = [
  http.get(Endpoints.FRIENDS.href, async () => {
    return HttpResponse.json({
      status: "ok",
      data: sampleFriends,
    });
  }),
];
