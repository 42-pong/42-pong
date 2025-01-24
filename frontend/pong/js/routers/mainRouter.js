import { ChatView } from "../components/views/ChatView";
import { HomeView } from "../components/views/HomeView";
import { MainView } from "../components/views/MainView";
import { NotFoundView } from "../components/views/NotFoundView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const mainRouter = (target) => {
  const routes = {
    [MainView.Paths.HOME]: Route.defaultRoute(HomeView),
    [MainView.Paths.CHAT]: Route.defaultRoute(ChatView),
  };
  const defaultRoute = Route.defaultRoute(NotFoundView);
  return new Router(target, defaultRoute, routes);
};
