import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createDefaultNavbar } from "../../utils/elements/nav/createDefaultNavbar";

export class MainNav extends Component {
  #nav;

  static links = Object.freeze([
    { name: "ホーム", path: Paths.HOME },
    { name: "チャット", path: Paths.CHAT },
    { name: "ユーザー一覧", path: Paths.USERS },
    { name: "フレンド一覧", path: Paths.FRIENDS },
    { name: "マイページ", path: Paths.MYPAGE },
  ]);

  _onConnect() {
    this.#nav = createDefaultNavbar(MainNav.links);

    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const link = event.target;
      if (link?.pathname === undefined) return;

      link.dispatchEvent(
        PongEvents.UPDATE_ROUTER.create(link.pathname),
      );
    });
  }

  _render() {
    this.appendChild(this.#nav);
  }
}
