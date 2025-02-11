// TODO: バックエンドのエントポイントベースを環境変数からのものになるように改善
const HOST = "localhost:8000";
const BASE_URL = new URL(`http://${HOST}`);
const WEBSOCKET_BASE_URL = new URL(`ws://${HOST}`);

export const Endpoints = Object.freeze({
  HEALTH: new URL("/api/health/", BASE_URL),
  WEBSOCKET: new URL("/ws/", WEBSOCKET_BASE_URL),
  USERS: {
    default: new URL("/api/users/", BASE_URL),
    withId: (userId) => new URL(`${userId}`, Endpoints.USERS.default),
  },
  TOKEN: new URL("/api/token/", BASE_URL),
  AUTH2: new URL("/oauth2/authorize/", BASE_URL),
});
