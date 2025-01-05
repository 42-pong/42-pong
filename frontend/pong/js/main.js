import "./components";
import { homeRouter } from "./routers/homeRouter";
import { initWebSocket } from "./websocket";

function main() {
  const app = document.getElementById("app");
  const router = homeRouter(app);

  initWebSocket();
  router.update(window.location.pathname);
}

async function enableMocking() {
  if (process.env.NODE_ENV !== "development") {
    return;
  }
  const { worker } = await import("./mocks/browser");
  return worker.start();
}

enableMocking().then(main);
