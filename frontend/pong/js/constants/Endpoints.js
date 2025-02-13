// TODO: バックエンドのエントポイントベースを環境変数からのものになるように改善
const HOST = "localhost:8000";
const BASE_URL = new URL(`http://${HOST}`);
const WEBSOCKET_BASE_URL = new URL(`ws://${HOST}`);

export const Endpoints = Object.freeze({
  create: (pathname) => new URL(pathname, BASE_URL),
  HEALTH: new URL("/api/health/", BASE_URL),
  WEBSOCKET: new URL("/ws/", WEBSOCKET_BASE_URL),
  USERS: {
    default: new URL("/api/users/", BASE_URL),
    withId: (userId) => new URL(`${userId}`, Endpoints.USERS.default),
  },
});
