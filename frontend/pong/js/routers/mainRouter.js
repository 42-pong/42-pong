import { ChatView } from "../components/views/ChatView";
import { HomeView } from "../components/views/HomeView";
import { MainView } from "../components/views/MainView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const mainRouter = (target) => {
  const routes = {
    [MainView.Paths.HOME]: Route.defaultRoute(HomeView),
    [MainView.Paths.CHAT]: Route.defaultRoute(ChatView),
  };
  return new Router(target, HomeView, routes);
};
