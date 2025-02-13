import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";

const SAMPLE_COUNT = 30;
const createSampleUser = (number) =>
  Object.freeze({
    id: `${number}`,
    username: `pong${number}`,
    display_name: `DISPLAY${number}`,
    avatar: "https://placehold.co/30",
  });
const sampleUsers = Array.from({ length: SAMPLE_COUNT }).map(
  (_, idx) => createSampleUser(idx + 1),
);

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
