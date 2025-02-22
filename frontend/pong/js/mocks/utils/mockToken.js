import { HttpResponse } from "msw";

const MOCK_EMAIL = "pong";
const MOCK_PASSWORD = "pong";
const MOCK_JWT_TOKEN_ACCESS = "mock-access";
const MOCK_JWT_TOKEN_REFRESH = "mock-refresh";

const verifyToken = (headers) => {
  const authHeader = headers.get("Authorization");

  return authHeader === `Bearer ${MOCK_JWT_TOKEN_ACCESS}`;
};

const notAuthenticatedHttpResponse = () =>
  new HttpResponse(
    JSON.stringify({
      detail: "Authentication credentials were not provided.",
    }),
    {
      status: 401,
      headers: {
        "Content-Type": "application/json",
      },
    },
  );

export {
  MOCK_EMAIL,
  MOCK_PASSWORD,
  MOCK_JWT_TOKEN_ACCESS,
  MOCK_JWT_TOKEN_REFRESH,
  verifyToken,
  notAuthenticatedHttpResponse,
};
