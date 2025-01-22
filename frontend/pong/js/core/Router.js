import { Route } from "./Route";

export class Router {
  #target;
  #view;
  #routes;
  #DefaultView;

  constructor(target, DefaultView, routes = {}) {
    this.#target = target;

    this.#view = null;

    this.#routes = Route.defaultRoutes(DefaultView);
    Object.assign(this.#routes, routes);

    this.#DefaultView = DefaultView;
  }

  update(path = this.#DefaultView._defaultPath) {
    const route = this.#findRoute(path);
    const isUpdated = this.#render(route);
    return isUpdated;
  }

  #findRoute(path) {
    if (path && this.#routes[path]) return this.#routes[path];
    return Route.defaultRoute(this.#DefaultView);
  }

  #mountView() {
    const currentView = this.#target.firstChild;

    if (currentView === this.#view) return false;

    if (currentView)
      this.#target.removeChild(this.#target.firstChild);
    this.#target.appendChild(this.#view);
    return true;
  }

  #render(route) {
    const { path, View } = route;
    let isUpdated;

    if (this.#view instanceof View)
      isUpdated = this.#view._updatePath(path);
    else {
      this.#view = new View({ path });
      isUpdated = this.#mountView();
    }
    return isUpdated;
  }
}
