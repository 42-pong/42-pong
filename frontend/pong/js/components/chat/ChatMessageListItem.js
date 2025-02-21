import { getUser } from "../../api/users/getUser";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { createNameplate } from "../../utils/elements/div/createNameplate";

export class ChatMessageListItem extends Component {
  constructor(state = {}) {
    super({ user: null, content: "...", ...state });
  }
  _setStyle() {
    BootstrapDisplay.setBlock(this);
  }

  _onConnect() {
    const { item: message } = this._getState();
    const { from, content } = message.data;
    getUser(from).then(({ user, error }) => {
      if (error) {
        console.warn(error);
        return;
      }
      this._updateState({ user, content });
    });
  }

  _render() {
    const { user, content } = this._getState();

    const message = createElement("span");
    message.textContent = content;

    this.append(createNameplate(user, "max(30px,3vh)"), message);
  }
}
