import { http, HttpResponse, delay } from "msw";
import { Endpoints } from "../../Endpoints";

export const handlers = [
  http.get(Endpoints.HEALTH.href, async () => {
    await delay(3000);
    return HttpResponse.json({
      status: "OK",
    });
  }),
];
