import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";

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
    const ul = getNavItemsList(MainNav.links);

    this.#nav = createElement("nav");
    // TODO: [DELETE] 一時的なスタイル指定
    this.#nav.innerHTML += `
    <style>
      nav {
        border-top: 1px solid black;
        border-bottom: 1px solid black;
      }
      nav ul{
        display: flex;
        justify-content: flex-start;
        align-items: center;
      }
      nav ul li{
        list-style: none;
        margin: 5px;
      }
    </style>`;
    this.#nav.appendChild(ul);

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

const getNavItemsList = (links) => {
  const ul = createElement("ul");

  for (const link of MainNav.links) {
    const anchor = createElement(
      "a",
      {
        textContent: link.name,
      },
      {
        href: link.path,
      },
    );

    const li = createElement("li");
    li.appendChild(anchor);

    ul.appendChild(li);
  }
  return ul;
};
