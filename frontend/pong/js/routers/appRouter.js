import { DashboardView } from "../components/views/DashboardView";
import { LoginView } from "../components/views/LoginView";
import { MainView } from "../components/views/MainView";
import { SignUpView } from "../components/views/SignUpView";
import { TournamentsView } from "../components/views/TournamentsView";
import { Paths } from "../constants/Paths";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const appRouter = (target) => {
  const routes = {
    [Paths.LOGIN]: Route.defaultRoute(LoginView),
    [Paths.SIGNUP]: Route.defaultRoute(SignUpView),
    [Paths.HOME]: Route.createRoute(MainView, MainView.Paths.HOME),
    [Paths.USERS]: Route.createRoute(MainView, MainView.Paths.USERS),
    [Paths.FRIENDS]: Route.createRoute(
      MainView,
      MainView.Paths.FRIENDS,
    ),
    [Paths.DASHBOARD]: Route.createRoute(
      MainView,
      MainView.Paths.DASHBOARD,
    ),
    [Paths.MYPAGE]: Route.createRoute(
      MainView,
      MainView.Paths.MYPAGE,
    ),
    [Paths.TOURNAMENTS]: Route.defaultRoute(TournamentsView),
  };
  const defaultRoute = Route.createRoute(
    MainView,
    MainView.Paths.NOT_FOUND,
  );
  return new Router(target, defaultRoute, routes);
};
