export class Router {
  #target;
  #defaultRoute;
  #view;
  #routes;

  constructor(target, DefaultView, defaultPath, routes) {
    this.#target = target;
    this.#defaultRoute = { path: defaultPath, View: DefaultView };
    this.#routes = { [defaultPath]: DefaultView };
    Object.assign(this.#routes, routes);
    this.#view = new DefaultView({ path: defaultPath });
  }

  #getRoute(path) {
    if (path && this.#routes[path]) return { path, View: this.#routes[path] };
    return this.#defaultRoute;
  }

  #update(route) {
    const { path, View } = route;
    if (this.#view instanceof View) return this.#view._updatePath(path);
    this.#view = new View({ path });
    this.load();
    return true;
  }

  router(requestedPath) {
    const route = this.#getRoute(requestedPath);
    const isUpdated = this.#update(route);
    return { isUpdated, path: route.path };
  }

  load() {
    if (this.#target.firstChild)
      this.#target.removeChild(this.#target.firstChild);
    this.#target.appendChild(this.#view);
  }
}
