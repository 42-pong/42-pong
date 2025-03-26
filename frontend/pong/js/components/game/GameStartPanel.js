import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createElement } from "../../utils/elements/createElement";
import { getTextContent } from "../../utils/i18n/lang";
import { MatchContainer } from "../match/MatchContainer";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";
import { LinkButton } from "../utils/LinkButton";

export class GameStartPanel extends Component {
  #listenIsSignedIn;

  constructor(state = {}) {
    super({ isPlayingMatch: false, ...state });

    this.#listenIsSignedIn = null;
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth50(this);
    BootstrapSizing.setHeight50(this);
  }

  _onConnect() {
    const isSignedIn =
      UserSessionManager.getInstance().myInfo.observe(
        ({ isSignedIn }) => isSignedIn,
      );
    Object.assign(this._state, { isSignedIn });

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

    this.#listenIsSignedIn = ({ isSignedIn }) => {
      this._updateState({ isSignedIn });
    };
    UserSessionManager.getInstance().myInfo.attach(
      this.#listenIsSignedIn,
    );
  }

  _onDisconnect() {
    UserSessionManager.getInstance().myInfo.detach(
      this.#listenIsSignedIn,
    );
    this.#listenIsSignedIn = null;
  }

  _render() {
    const { isPlayingMatch } = this._getState();

    if (isPlayingMatch) this.append(new MatchContainer());
    else {
      const { isSignedIn } = this._getState();
      const menu = createMenu(isSignedIn);
      BootstrapDisplay.setGrid(menu);
      BootstrapSizing.setWidth50(menu);
      BootstrapSpacing.setGap(menu);

      this.append(menu);
    }
  }
}

const createMenu = (isSignedIn) => {
  const tournamentStartButton = new LinkButton(
    {
      textContent: getTextContent("remoteTournament"),
      pathname: Paths.TOURNAMENTS,
    },
    { type: "button" },
  );
  tournamentStartButton.setPrimary();
  if (!isSignedIn) tournamentStartButton.setDisabled();

  const localMatchStartButton = new EventDispatchingButton(
    { textContent: getTextContent("localMatch") },
    { type: "button" },
    PongEvents.START_MATCH,
  );
  localMatchStartButton.setOutlinePrimary();

  const container = createElement("div");
  container.append(tournamentStartButton, localMatchStartButton);
  return container;
};
