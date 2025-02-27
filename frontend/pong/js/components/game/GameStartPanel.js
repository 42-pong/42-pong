import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { MatchContainer } from "../match/MatchContainer";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";
import { LinkButton } from "../utils/LinkButton";

export class GameStartPanel extends Component {
  #menu;

  constructor(state = {}) {
    super({ isPlayingMatch: false, ...state });
  }

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
      PongEvents.START_MATCH.type,
      (event) => {
        event.preventDefault();
        this._updateState({ isPlayingMatch: true });
      },
    );

    this._attachEventListener(PongEvents.END_MATCH.type, (event) => {
      event.preventDefault();
      this._updateState({ isPlayingMatch: false });
    });
  }

  _render() {
    const { isPlayingMatch } = this._getState();

    if (isPlayingMatch) this.append(new MatchContainer());
    else this.appendChild(this.#menu);
  }
}

const createMenu = () => {
  const tournamentStartButton = new LinkButton(
    { textContent: "トーナメント開始", pathname: Paths.TOURNAMENTS },
    { type: "button" },
  );
  tournamentStartButton.setPrimary();

  const localMatchStartButton = new EventDispatchingButton(
    { textContent: "ローカル対戦" },
    { type: "button" },
    PongEvents.START_MATCH,
  );
  localMatchStartButton.setOutlinePrimary();

  const container = createElement("div");
  container.append(tournamentStartButton, localMatchStartButton);
  return container;
};
