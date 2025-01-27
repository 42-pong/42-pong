import { View } from "../../core/View";
import { mainRouter } from "../../routers/mainRouter";
import { createElement } from "../../utils/elements/createElement";
import { MainNav } from "../navs/MainNav";

export class MainView extends View {
  #nav;
  #main;
  #mainRouter;

  // MainView の対応中のパスを列挙
  static Paths = Object.freeze({
    HOME: "/",
    CHAT: "/chat",
    USERS: "/users",
    FRIENDS: "/friends",
    MYPAGE: "/mypage",
    TOURNAMENTS: "/tournaments",
    NOT_FOUND: "/not-found",
  });

  _onConnect() {
    this.#nav = new MainNav();
    this.#main = createElement("div");
    this.#mainRouter = mainRouter(this.#main);
  }

  #updateMain() {
    const path = this._getPath();
    this.#mainRouter.update(path);
  }

  _render() {
    this.#updateMain();
    this.appendChild(this.#nav);
    this.appendChild(this.#main);
  }

  _update() {
    this.#updateMain();
  }
}
