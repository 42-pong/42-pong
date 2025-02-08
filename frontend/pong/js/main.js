import "./components";
import { PongEvents } from "./constants/PongEvents";
import { appRouter } from "./routers/appRouter";
import { initWebSocket } from "./websocket";

function main() {
  const app = document.getElementById("app");
  const router = appRouter(app);
  const updateWindowPath = () => {
    router.update(window.location.pathname);
  };

  app.addEventListener(PongEvents.UPDATE_ROUTER.type, (event) => {
    const { path } = event.detail;
    const isUpdated = router.update(path);
    if (isUpdated) window.history.pushState({}, "", path);
  });
  window.addEventListener("popstate", updateWindowPath);
  initWebSocket();
  updateWindowPath();
}

async function enableMocking() {
  if (process.env.NODE_ENV !== "development") {
    return;
  }
  const { worker } = await import("./mocks/browser");
  return worker.start();
}

enableMocking().then(main);
