import "./components";
import { ErrorView } from "./components/views/ErrorView";
import { MainView } from "./components/views/MainView";
import { PongEvents } from "./constants/PongEvents";
import { Route } from "./core/Route";
import { appRouter } from "./routers/appRouter";
import { UserSessionManager } from "./session/UserSessionManager";
import { handleAuthPath } from "./utils/handleAuthPath";

function main() {
  const app = document.getElementById("app");
  const appLocal = document.getElementById("app-local");
  const appGlobal = document.getElementById("app-global");
  const router = appRouter(appLocal);
  const updateWindowPath = async () => {
    if (await handleAuthPath()) return;
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
      router.display(Route.defaultRoute(ErrorView)),
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
