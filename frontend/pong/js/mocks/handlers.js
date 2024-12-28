import { http, HttpResponse, delay } from "msw";
import endpoints from "../endpoints";

export const handlers = [
  http.get(endpoints.health.href, async () => {
    await delay(3000);
    return HttpResponse.json({
      status: "OK",
    });
  }),
];
