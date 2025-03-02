import { HttpResponse } from "msw";

export const simpleErrorResponse = () =>
  new HttpResponse(
    JSON.stringify({
      status: "error",
    }),
    {
      status: 400,
      headers: {
        "Content-Type": "application/json",
      },
    },
  );
