const PORT = import.meta.env.VITE_PORT || 8080;
const HOST = `localhost:${PORT}`;
const BASE_URL = new URL(`https://${HOST}`);
const WEBSOCKET_BASE_URL = new URL(`wss://${HOST}`);

const DEFAULT_AVATAR_IMAGE_PATH = "/media/avatars/sample.png";

export const Endpoints = Object.freeze({
  create: (pathname) => new URL(pathname, BASE_URL),
  HEALTH: new URL("/api/health/", BASE_URL),
  WEBSOCKET: new URL("/ws/", WEBSOCKET_BASE_URL),
  USERS: {
    default: new URL("/api/users/", BASE_URL),
    withId: (userId) =>
      new URL(`${userId}/`, Endpoints.USERS.default),
    me: () => new URL("me/", Endpoints.USERS.default),
    defaultAvatar: new URL(DEFAULT_AVATAR_IMAGE_PATH, BASE_URL),
  },
  TOKEN: new URL("/api/token/", BASE_URL),
  REFRESH_TOKEN: new URL("/api/token/refresh/", BASE_URL),
  FRIENDS: {
    default: new URL("/api/users/me/friends/", BASE_URL),
    withId: (friendId) =>
      new URL(`${friendId}/`, Endpoints.FRIENDS.default),
  },
  BLOCKS: {
    default: new URL("/api/users/me/blocks/", BASE_URL),
    withId: (blockedUserId) =>
      new URL(`${blockedUserId}/`, Endpoints.BLOCKS.default),
  },
  PARTICIPATIONS: new URL(
    "/api/tournaments/participations/",
    BASE_URL,
  ),
  TOURNAMENTS: {
    default: new URL("/api/tournaments/", BASE_URL),
    withId: (tournamentId) =>
      new URL(`${tournamentId}/`, Endpoints.TOURNAMENTS.default),
  },
  MATCHES: {
    default: new URL("/api/matches/", BASE_URL),
    withId: (matchId) =>
      new URL(`${matchId}/`, Endpoints.MATCHES.default),
  },

  ACCOUNTS: new URL("/api/accounts/", BASE_URL),
  OAUTH: new URL("/api/oauth2/authorize/", BASE_URL),
});
