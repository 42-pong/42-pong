import { HomeView } from "../components/views/HomeView";
import { AboutView } from "../components/views/AboutView";
import { LoginView } from "../components/views/LoginView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const homeRouter = (target) => {
  const routes = {
    "/": Route.defaultRoute(HomeView),
    "/about": Route.createRoute(AboutView, "/about"),
    "/login": Route.createRoute(LoginView, "/login"),
    "/about2": Route.createRoute(HomeView, "/tmp"),
    "/about3": Route.createRoute(HomeView, "/no-exist"),
  };
  return new Router(target, HomeView, routes);
};
