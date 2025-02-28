import { ErrorView } from "../components/views/ErrorView";
import { FriendsView } from "../components/views/FriendsView";
import { HomeView } from "../components/views/HomeView";
import { LoadingView } from "../components/views/LoadingView";
import { MainView } from "../components/views/MainView";
import { MyPageView } from "../components/views/MyPageView";
import { NotFoundView } from "../components/views/NotFoundView";
import { TournamentsView } from "../components/views/TournamentsView";
import { UsersView } from "../components/views/UsersView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const mainRouter = (target) => {
  const routes = {
    [MainView.Paths.HOME]: Route.defaultRoute(HomeView),
    [MainView.Paths.USERS]: Route.defaultRoute(UsersView),
    [MainView.Paths.FRIENDS]: Route.defaultRoute(FriendsView),
    [MainView.Paths.MYPAGE]: Route.defaultRoute(MyPageView),
    [MainView.Paths.TOURNAMENTS]: Route.defaultRoute(TournamentsView),
    [MainView.Paths.NOT_FOUND]: Route.defaultRoute(NotFoundView),
    [MainView.Paths.LOADING]: Route.defaultRoute(LoadingView),
    [MainView.Paths.ERROR]: Route.defaultRoute(ErrorView),
  };
  const defaultRoute = Route.defaultRoute(NotFoundView);
  return new Router(target, defaultRoute, routes);
};
