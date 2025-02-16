import "./components";
import { ChatGlobal } from "./components/chat/ChatGlobal";
import { PongEvents } from "./constants/PongEvents";
import { appRouter } from "./routers/appRouter";
import { initWebSocket } from "./websocket";

function main() {
  const appLocal = document.getElementById("app-local");
  const router = appRouter(appLocal);
  const updateWindowPath = () => {
    router.update(window.location.pathname);
  };

  const app = document.getElementById("app");
  app.addEventListener(PongEvents.UPDATE_ROUTER.type, (event) => {
    const { path } = event.detail;
    const isUpdated = router.update(path);
    if (isUpdated) window.history.pushState({}, "", path);
  });
  window.addEventListener("popstate", updateWindowPath);
  initWebSocket();

  const appGlobal = document.getElementById("app-global");
  initGlobalFeatures(appGlobal);
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

const initGlobalFeatures = (globalRoot) => {
  const chatFeature = new ChatGlobal();

  globalRoot.append(chatFeature);
};
