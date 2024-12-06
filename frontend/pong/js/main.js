import "./components";
import { HomeView } from "./components/view/HomeView";
import { SignoutView } from "./components/view/SignoutView";
import { Router } from "./core/Router";

const app = document.getElementById("app");
const router = new Router(app, HomeView, "/", {
  "/about": HomeView,
  "/signout": SignoutView,
});

router.load();

app.addEventListener("router", (event) => {
  const targetPath = event.detail ? event.detail.path : "/";
  const { isUpdated, path } = router.router(targetPath);
  if (isUpdated) window.history.pushState({}, "", path);
});

window.onpopstate = () => {
  router.router(window.location.pathname);
};
