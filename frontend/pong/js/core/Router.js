import { Route } from "./Route";

export class Router {
  #target;
  #view;
  #routes;
  #defaultRoute;

  constructor(target, defaultRoute, routes = {}) {
    this.#target = target;

    this.#view = null;

    this.#routes = routes;

    this.#defaultRoute = defaultRoute;
  }

  update(path) {
    const route = this.#findRoute(path);
    const isUpdated = this.#render(route);
    return isUpdated;
  }

  display(route) {
    if (!(route instanceof Route)) return;
    const isUpdated = this.#render(route);
    return isUpdated;
  }

  #findRoute(path) {
    if (path && this.#routes[path]) return this.#routes[path];
    return this.#defaultRoute;
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
