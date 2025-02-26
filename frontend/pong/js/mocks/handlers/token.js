import { http, HttpResponse } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import {
  MOCK_EMAIL,
  MOCK_JWT_TOKEN_ACCESS,
  MOCK_JWT_TOKEN_REFRESH,
  MOCK_PASSWORD,
} from "../utils/mockToken";

export const handlers = [
  http.post(Endpoints.TOKEN.href, async ({ request }) => {
    const { email, password } = await request.json();
    const isValidCredentials =
      email === MOCK_EMAIL && password === MOCK_PASSWORD;
    return createTokenResponse(isValidCredentials);
  }),
  http.post(Endpoints.REFRESH_TOKEN.href, async ({ request }) => {
    const { refresh } = await request.json();
    const isValidRefreshToken = refresh === MOCK_JWT_TOKEN_REFRESH;
    return createRefreshTokenResponse(isValidRefreshToken);
  }),
];

const createTokenResponse = (isValidCredentials) =>
  isValidCredentials
    ? HttpResponse.json({
        status: "ok",
        data: {
          access: MOCK_JWT_TOKEN_ACCESS,
          refresh: MOCK_JWT_TOKEN_REFRESH,
        },
      })
    : new HttpResponse(
        JSON.stringify({ status: "error", code: "not_exists" }),
        {
          status: 401,
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

const createRefreshTokenResponse = (isValidRefreshToken) =>
  isValidRefreshToken
    ? HttpResponse.json({
        status: "ok",
        data: {
          access: MOCK_JWT_TOKEN_ACCESS,
        },
      })
    : new HttpResponse(
        JSON.stringify({ status: "error", code: "invalid" }),
        {
          status: 401,
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
