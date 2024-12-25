// TODO: バックエンドのエントポイントベースを環境変数からのものになるように改善
const baseUrl = new URL("http://localhost:8000");

export default {
  health: new URL("/api/health/", baseUrl),
};
