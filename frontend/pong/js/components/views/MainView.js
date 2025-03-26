import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { View } from "../../core/View";
import { mainRouter } from "../../routers/mainRouter";
import { createElement } from "../../utils/elements/createElement";
import { MainNavbar } from "../navigation/MainNavbar";

export class MainView extends View {
  #navbar;
  #main;
  #mainRouter;

  // MainView の対応中のパスを列挙
  static Paths = Object.freeze({
    HOME: "/",
    USERS: "/users",
    FRIENDS: "/friends",
    DASHBOARD: "/dashboard",
    MYPAGE: "/mypage",
    TOURNAMENTS: "/tournaments",
    NOT_FOUND: "/not-found",
    LOADING: "/loading",
    ERROR: "/error",
  });

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapSizing.setViewportHeight100(this);
    BootstrapSpacing.setPadding(this);

    BootstrapFlex.setFlexGrow1(this.#main);
  }

  _onConnect() {
    this.#navbar = new MainNavbar();
    this.#main = createElement("div");
    this.#mainRouter = mainRouter(this.#main);
  }

  #updateMain() {
    const path = this._getPath();
    this.#mainRouter.update(path);
  }

  _render() {
    this.#updateMain();
    this.appendChild(this.#navbar);
    this.appendChild(this.#main);
  }

  _update() {
    this.#updateMain();
  }
}
