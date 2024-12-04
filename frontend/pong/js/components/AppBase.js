import { Component } from "../core/Component";
import { HomePage } from "./page/HomePage";

export class AppBase extends Component {
  #PageComponent;
  #path;
  #page;

  getPageComponent() {
    return this.#PageComponent;
  }

  setPage(PageComponent, path) {
    this.#PageComponent = PageComponent;
    this.#path = path;
  }

  updatePath(path) {
    if (this.#path === path) return;
    this.#page._setState({ path });
  }

  constructor() {
    super();
    this.#PageComponent = HomePage;
    this.#path = "/";
    this.#page = null;
    console.log("AppBase: constructor");
  }

  _init() {
    this._name = "app-base";
  }

  _render() {
    if (this.firstChild) this.removeChild();
    this.#page = new this.#PageComponent(this.#path);
    this.appendChild(this.#page);
    // this.innerHTML = this._getTemplate();
  }
}
