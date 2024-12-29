// TODO: バックエンドのエントポイントベースを環境変数からのものになるように改善
const BASE_URL = new URL("http://localhost:8000");
const WEBSOCKET_BASE_URL = new URL("ws://localhost:8000/ws/match/");

export const Endpoints = Object.freeze({
  HEALTH: new URL("/api/health/", BASE_URL),
  WEBSOCKET_BASE_URL,
});
