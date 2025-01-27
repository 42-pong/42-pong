import { View } from "../../core/View";
import { mainRouter } from "../../routers/mainRouter";
import { MainNav } from "../navs/MainNav";

export class MainView extends View {
  #router;
  #nav;
  #main;

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
    this.#router = mainRouter(this.#main);
  }

  _render() {
    const path = this._getPath();
    this.#router.update(path);

    this.appendChild(this.#nav);
    this.appendChild(this.#main);
  }

  _update() {
    const path = this._getPath();
    this.#router.update(path);
  }
}
