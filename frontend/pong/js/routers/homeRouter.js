import { HomeView } from "../components/views/HomeView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const homeRouter = (target) => {
  const routes = {
    "/": Route.defaultRoute(HomeView),
    "/about": Route.createRoute(HomeView, "/about"),
    "/about1": Route.createRoute(HomeView, "/about"),
    "/about2": Route.createRoute(HomeView, "/tmp"),
    "/about3": Route.createRoute(HomeView, "/no-exist"),
  };
  return new Router(target, HomeView, routes);
};
