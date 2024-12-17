export class Route {
  #View;
  #path;

  constructor(View, path = "/") {
    this.#View = View;
    this.#path = path;
  }

  get path() {
    return this.#path;
  }

  get View() {
    return this.#View;
  }

  static createRoute(View, path) {
    return new Route(View, path);
  }

  static defaultRoute(View) {
    return Route.createRoute(View, View._defaultPath);
  }

  static defaultRoutes(View) {
    return { [View._defaultPath]: Route.defaultRoute(View) };
  }
}
