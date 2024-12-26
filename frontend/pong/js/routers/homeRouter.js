import { HomeView } from "../components/views/HomeView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const homeRouter = (target) => {
  const routes = {
    "/": Route.defaultRoute(HomeView),
  };
  return new Router(target, HomeView, routes);
};
