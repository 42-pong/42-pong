// TODO: バックエンドのエントポイントベースを環境変数からのものになるように改善
const HOST = "localhost:8000";
const BASE_URL = new URL(`http://${HOST}`);
const WEBSOCKET_BASE_URL = new URL(`ws://${HOST}`);

const DEFAULT_AVATAR_IMAGE_PATH = "/media/avatars/sample.png";

export const Endpoints = Object.freeze({
  create: (pathname) => new URL(pathname, BASE_URL),
  HEALTH: new URL("/api/health/", BASE_URL),
  WEBSOCKET: new URL("/ws/", WEBSOCKET_BASE_URL),
  USERS: {
    default: new URL("/api/users/", BASE_URL),
    withId: (userId) => new URL(`${userId}`, Endpoints.USERS.default),
    me: () => new URL("me/", Endpoints.USERS.default),
    defaultAvatar: new URL(DEFAULT_AVATAR_IMAGE_PATH, BASE_URL),
  },
  TOKEN: new URL("/api/token/", BASE_URL),
  REFRESH_TOKEN: new URL("/api/token/refresh/", BASE_URL),
  FRIENDS: new URL("/api/users/me/friends/", BASE_URL),
  PARTICIPATIONS: new URL(
    "/api/tournaments/participations/",
    BASE_URL,
  ),
});
