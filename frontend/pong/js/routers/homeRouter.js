import { HomeView } from "../components/view/HomeView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const homeRouter = (target) => {
  const routes = {
    "/": Route.createRoute(HomeView, "/"),
  };
  return new Router(target, HomeView, routes);
};
