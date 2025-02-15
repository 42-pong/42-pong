import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapBackground } from "../../bootstrap/utilities/background";
import { BootstrapPosition } from "../../bootstrap/utilities/position";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";
import { ChatPanel } from "./ChatPanel";

export class ChatGlobal extends Component {
  #toggleButton;

  constructor(state = {}) {
    super({ isPanelOn: false, ...state });
  }

  _setStyle() {
    BootstrapPosition.setFixed(this);
    BootstrapPosition.setBottom(this);
    BootstrapPosition.setEnd(this);
    BootstrapBackground.setLight(this);

    BootstrapGrid.setCol(this, 6);
    BootstrapGrid.setCol(this, 5, "md");
    BootstrapGrid.setCol(this, 4, "lg");
    BootstrapGrid.setCol(this, 3, "xl");

    this.#toggleButton.setOutlineSecondary();
  }

  _onConnect() {
    this.#toggleButton = new EventDispatchingButton(
      { textContent: "💬 チャット" },
      { type: "button" },
      PongEvents.TOGGLE_CHAT_GLOBAL,
    );

    this._attachEventListener(
      PongEvents.TOGGLE_CHAT_GLOBAL.type,
      () => {
        const { isPanelOn } = this._getState();
        this._updateState({ isPanelOn: !isPanelOn });
      },
    );
  }

  _render() {
    const { isPanelOn } = this._getState();
    if (isPanelOn) {
      this.append(new ChatPanel());
    }

    this.append(this.#toggleButton);
  }
}
