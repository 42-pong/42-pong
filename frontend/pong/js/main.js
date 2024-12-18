import "./components";
import { homeRouter } from "./routers/homeRouter.js";

const move = (router, path) => {
  const isUpdated = router.update(path);
  if (isUpdated) window.history.pushState({}, "", path);
};

const app = document.getElementById("app");
const router = homeRouter(app);

// browser のナヴィゲーション時のイベント対応
window.addEventListener("popstate", () => {
  console.log("POPUP!", window.location.pathname);
  router.update(window.location.pathname);
});

// HomeView からのカスタムイベント対応
app.addEventListener("router", (event) => {
  const path = event.detail ? event.detail.path : "/";
  move(router, path);
});

// 最初の app 更新
router.update(window.location.pathname);
