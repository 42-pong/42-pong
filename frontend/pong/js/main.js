import "./components";
import { AppBase } from "./components/AppBase";
import { HomePage } from "./components/page/HomePage";

const appDiv = document.getElementById("app");
const app = new AppBase();
appDiv.appendChild(app);

const routes = {
  "/": HomePage,
  "/about": HomePage,
};

const router = (url) => {
  const path = !url || routes[url] ? "/" : url;
  const PageComponent = routes[path];
  window.history.pushState({}, "", path);

  if (app.getPageComponent() === PageComponent) {
    app.updatePath(path);
  } else {
    app.setPage(page, path);
  }
};

window.onpopstate = router;
