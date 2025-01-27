import { LoginView } from "../components/views/LoginView";
import { MainView } from "../components/views/MainView";
import { Paths } from "../constants/Paths";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const appRouter = (target) => {
  const routes = {
    [Paths.LOGIN]: Route.defaultRoute(LoginView),
    [Paths.HOME]: Route.createRoute(MainView, MainView.Paths.HOME),
    [Paths.CHAT]: Route.createRoute(MainView, MainView.Paths.CHAT),
  };
  const defaultRoute = Route.createRoute(
    MainView,
    MainView.Paths.NOT_FOUND,
  );
  return new Router(target, defaultRoute, routes);
};
