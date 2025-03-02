import { HttpResponse } from "msw";

export const simpleDeleteResponse = () =>
  new HttpResponse(null, {
    status: 204,
  });
