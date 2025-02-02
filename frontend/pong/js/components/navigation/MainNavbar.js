import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createDefaultNavbar } from "../../utils/elements/nav/createDefaultNavbar";

export class MainNavbar extends Component {
  #navbar;

  static links = Object.freeze([
    { name: "ホーム", path: Paths.HOME },
    { name: "チャット", path: Paths.CHAT },
    { name: "ユーザー一覧", path: Paths.USERS },
    { name: "フレンド一覧", path: Paths.FRIENDS },
    { name: "マイページ", path: Paths.MYPAGE },
  ]);

  _onConnect() {
    this.#navbar = createDefaultNavbar(MainNavbar.links);

    this._attachEventListener(
      "click",
      PongEvents.UPDATE_ROUTER.trigger,
    );
  }

  _render() {
    this.appendChild(this.#navbar);
  }
}
