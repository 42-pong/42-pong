import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createPrimaryButton } from "../../utils/elements/button/createPrimaryButton";
import { createElement } from "../../utils/elements/createElement";

export class GameStartPanel extends Component {
  #menu;

  #setStyle() {
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
    const menu = createElement("div");
    menu.appendChild(getLocalMatchStartButton());
    menu.appendChild(getTournamentStartButton());
    this.#menu = menu;

    this.#setStyle();

    this._attachEventListener(
      "click",
      PongEvents.UPDATE_ROUTER.trigger,
    );
  }

  _render() {
    this.appendChild(this.#menu);
  }
}

const getLocalMatchStartButton = () => {
  const localMatchStartButton = createPrimaryButton(
    { textContent: "ローカル対戦" },
    { type: "button" },
  );
  // TODO: [DELETE] ローカルマッチの準備とともに削除
  localMatchStartButton.setAttribute("disabled", "");
  return localMatchStartButton;
};

const getTournamentStartButton = () => {
  const tournamentStartButton = createPrimaryButton(
    { textContent: "トーナメント開始", pathname: Paths.TOURNAMENTS },
    { type: "button" },
  );
  return tournamentStartButton;
};
