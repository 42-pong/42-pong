import { HomeView } from "../components/views/HomeView";
import { LoginView } from "../components/views/LoginView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const homeRouter = (target) => {
  const routes = {
    "/": Route.defaultRoute(HomeView),
    "/login": Route.defaultRoute(LoginView),
  };
  return new Router(target, HomeView, routes);
};
