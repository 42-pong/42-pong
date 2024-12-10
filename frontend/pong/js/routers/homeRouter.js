import { ChatView } from "../components/view/ChatView";
import { HomeView } from "../components/view/HomeView";
import { SignoutView } from "../components/view/SignoutView";
import { Route } from "../core/Route";
import { Router } from "../core/Router";

export const homeRouter = (target) => {
  const homeRoutes = {
    "/": Route.createRoute(HomeView, "/"),
    "/about": Route.createRoute(HomeView, "/about"),
    "/signout": Route.createRoute(SignoutView, "/signout"),
    "/chat": Route.createRoute(ChatView, "/chat"),
  };
  return new Router(target, HomeView, homeRoutes);
};
