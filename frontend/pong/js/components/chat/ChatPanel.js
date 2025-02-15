import { BootstrapBackground } from "../../bootstrap/utilities/background";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { setHeight } from "../../utils/elements/style/setHeight";
import { ChatBuddyListContainer } from "./ChatBuddyListContainer";
import { ChatDmContainer } from "./ChatDmContainer";

export class ChatPanel extends Component {
  constructor(state = {}) {
    super({ isUserSelected: false, userId: "", ...state });
  }

  _setStyle() {
    BootstrapDisplay.setBlock(this);
    BootstrapBackground.setDarkSubtle(this);
    BootstrapBorders.setRounded(this);
    setHeight(this, "30vh");
  }

  _onConnect() {
    this._attachEventListener(
      PongEvents.UPDATE_USER_ID.type,
      (event) => {
        const {
          detail: { userId },
        } = event;
        if (!userId) return;

        this._updateState({ isUserSelected: true, userId });
      },
    );

    this._attachEventListener(
      PongEvents.TOGGLE_CHAT_USER_SELECTION.type,
      (event) => {
        const { isUserSelected } = this._getState();
        this._updateState({ isUserSelected: !isUserSelected });
      },
    );
  }

  _render() {
    const { isUserSelected, userId } = this._getState();

    const container = isUserSelected
      ? new ChatDmContainer({ userId })
      : new ChatBuddyListContainer();
    this.append(container);
  }
}
