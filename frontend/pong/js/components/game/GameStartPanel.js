import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { LinkButton } from "../utils/LinkButton";

export class GameStartPanel extends Component {
  #menu;

  _setStyle() {
    BootstrapDisplay.setGrid(this.#menu);
    BootstrapSizing.setWidth50(this.#menu);
    BootstrapSpacing.setGap(this.#menu);

    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth50(this);
    BootstrapSizing.setHeight50(this);
  }

  _onConnect() {
    this.#menu = createMenu();

    this._attachEventListener(
      "click",
      PongEvents.UPDATE_ROUTER.trigger,
    );
  }

  _render() {
    this.appendChild(this.#menu);
  }
}

const createMenu = () => {
  const tournamentStartButton = new LinkButton(
    { textContent: "トーナメント開始", pathname: Paths.TOURNAMENTS },
    { type: "button" },
  );
  // TODO: DELETE "disabled": ローカルマッチの準備とともに削除
  const localMatchStartButton = new LinkButton(
    { textContent: "ローカル対戦" },
    { type: "button", disabled: "" },
  );

  tournamentStartButton.setPrimary();
  localMatchStartButton.setOutlinePrimary();

  const container = createElement("div");
  container.appendChild(tournamentStartButton);
  container.appendChild(localMatchStartButton);
  return container;
};
