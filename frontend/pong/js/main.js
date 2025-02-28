import "./components";
import { MainView } from "./components/views/MainView";
import { PongEvents } from "./constants/PongEvents";
import { Route } from "./core/Route";
import { appRouter } from "./routers/appRouter";
import { UserSessionManager } from "./session/UserSessionManager";

function main() {
  const app = document.getElementById("app");
  const appLocal = document.getElementById("app-local");
  const appGlobal = document.getElementById("app-global");
  const router = appRouter(appLocal);
  const updateWindowPath = () => {
    router.update(window.location.pathname);
  };
  window.addEventListener("popstate", updateWindowPath);

  app.addEventListener(PongEvents.UPDATE_ROUTER.type, (event) => {
    const { path } = event.detail;
    const isUpdated = router.update(path);
    if (isUpdated) window.history.pushState({}, "", path);
  });

  UserSessionManager.getInstance().main({
    app,
    appLocal,
    appGlobal,
    updateWindowPath,
    displayMainLoading: () =>
      router.display(
        Route.createRoute(MainView, MainView.Paths.LOADING),
      ),
    displayMainError: () =>
      router.display(
        Route.createRoute(MainView, MainView.Paths.ERROR),
      ),
  });
}

async function enableMocking() {
  if (process.env.NODE_ENV !== "development") {
    return;
  }
  const { worker } = await import("./mocks/browser");
  return worker.start();
}

enableMocking().then(main);
