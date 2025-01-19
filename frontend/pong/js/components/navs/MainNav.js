import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";

export class MainNav extends Component {
  #nav;

  static links = Object.freeze([
    { name: "ホーム", path: Paths.HOME },
    { name: "チャット", path: Paths.CHAT },
  ]);

  _onConnect() {
    const ul = document.createElement("ul");
    for (const link of MainNav.links) {
      const anchor = document.createElement("a");
      anchor.textContent = link.name;
      anchor.href = link.path;

      const li = document.createElement("li");
      li.appendChild(anchor);

      ul.appendChild(li);
    }

    this.#nav = document.createElement("nav");
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
