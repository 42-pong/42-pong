import { getUser } from "../../api/users/getUser";
import { BootstrapText } from "../../bootstrap/utilities/text";
import { Component } from "../../core/Component";
import { createNameplate } from "../../utils/elements/div/createNameplate";

export class PlayerProfile extends Component {
  constructor(state) {
    super({ participation: null, user: null, ...state });
  }

  _setStyle() {
    BootstrapText.setTextCenter(this);
  }

  _onConnect() {
    const { participation } = this._getState();
    if (!participation) return;

    const { displayName, userId } = participation;

    getUser(userId).then(({ user, error }) => {
      if (error) return;
      this._updateState({ user: { ...user, displayName } });
    });
  }

  _render() {
    const { user } = this._getState();
    this.append(createNameplate(user, "max(20px, 5vh)"));
  }
}
